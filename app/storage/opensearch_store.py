import os
import time
import socket
from urllib.parse import urlparse
import httpx
from typing import Dict, Any, Optional, Tuple, List
from app.config import settings


class OpenSearchStore:
    """
    OpenSearch Searchable Representation Storage Adapter.
    Indexes canonical ULPF-IR normalized events for high-throughput search and analytics.
    Gracefully degrades if OpenSearch is initializing or offline.
    """

    def __init__(
        self,
        url: Optional[str] = None,
        index_name: Optional[str] = None,
    ):
        self.url = (url or settings.opensearch_url).rstrip("/")
        self.index_name = index_name or settings.opensearch_index
        self._index_initialized = False
        self._is_online: Optional[bool] = False
        self._last_check_time = 0.0
        self._check_interval = 30.0  # seconds
        self._http_client = httpx.Client(timeout=5.0)

    def is_available(self) -> bool:
        """Fast connectivity check with socket pre-check and circuit breaker."""
        now = time.time()
        if self._is_online is True:
            return True
        if self._is_online is False and (now - self._last_check_time) < self._check_interval:
            return False

        self._last_check_time = now

        # 1. Fast socket connectivity check (0.15s timeout)
        try:
            parsed = urlparse(self.url)
            host = parsed.hostname or self.url.split("://")[-1].split(":")[0]
            port = parsed.port or (443 if parsed.scheme == "https" else 9200)
            if host in ("minio", "opensearch", "redpanda", "kafka") and not os.path.exists("/.dockerenv"):
                self._is_online = False
                return False
            with socket.create_connection((host, port), timeout=0.15):
                pass
        except Exception:
            self._is_online = False
            return False

        # 2. HTTP Health check
        try:
            client = self._http_client
            if True:
                res = client.get(f"{self.url}/_cluster/health")
                self._is_online = (res.status_code == 200)
                return self._is_online
        except Exception:
            self._is_online = False
            return False

    def ensure_index(self) -> bool:
        """Create OpenSearch index with proper schema mappings if it does not exist."""
        if self._index_initialized:
            return True
        if not self.is_available():
            return False

        mapping = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0,
                "refresh_interval": "1s",
            },
            "mappings": {
                "properties": {
                    "event_id": {"type": "keyword"},
                    "raw_event_id": {"type": "keyword"},
                    "timestamp": {"type": "date"},
                    "source": {"type": "keyword"},
                    "vendor": {"type": "keyword"},
                    "product": {"type": "keyword"},
                    "format": {"type": "keyword"},
                    "event_type": {"type": "keyword"},
                    "action": {"type": "keyword"},
                    "severity": {"type": "keyword"},
                    "src_ip": {"type": "ip"},
                    "dst_ip": {"type": "ip"},
                    "parser": {"type": "keyword"},
                    "status": {"type": "keyword"},
                    "sha256": {"type": "keyword"},
                    "raw_message": {"type": "text"},
                }
            },
        }

        try:
            client = self._http_client
            if True:
                res = client.head(f"{self.url}/{self.index_name}")
                if res.status_code == 200:
                    self._index_initialized = True
                    return True
                elif res.status_code == 404:
                    put_res = client.put(f"{self.url}/{self.index_name}", json=mapping)
                    if put_res.status_code in (200, 201):
                        self._index_initialized = True
                        return True
        except Exception:
            self._is_online = False
        return False

    def index_event(self, event_id: str, document: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Index normalized event in OpenSearch.
        Returns (success: bool, status: str).
        """
        if self.is_available():
            try:
                self.ensure_index()
                doc_url = f"{self.url}/{self.index_name}/_doc/{event_id}"
                client = self._http_client
                if True:
                    resp = client.put(doc_url, json=document)
                    if resp.status_code in (200, 201):
                        return True, "indexed_opensearch"
            except Exception:
                self._is_online = False

        return False, "degraded_sqlite_fallback"

    def search_events(
        self,
        search_term: Optional[str] = None,
        filters: Optional[Dict[str, str]] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> Optional[Dict[str, Any]]:
        """Search indexed events via OpenSearch Query DSL."""
        if not self.is_available():
            return None

        try:
            must_clauses: List[Dict[str, Any]] = []

            if search_term:
                must_clauses.append({
                    "multi_match": {
                        "query": search_term,
                        "fields": [
                            "event_id",
                            "raw_message",
                            "src_ip",
                            "dst_ip",
                            "source",
                            "vendor",
                            "format",
                            "action",
                            "status",
                        ],
                    }
                })

            if filters:
                for k, v in filters.items():
                    if v:
                        must_clauses.append({"term": {k: v}})

            query_body: Dict[str, Any] = {
                "size": limit,
                "from": offset,
                "sort": [{"timestamp": {"order": "desc"}}, {"_score": {"order": "desc"}}],
            }

            if must_clauses:
                query_body["query"] = {"bool": {"must": must_clauses}}
            else:
                query_body["query"] = {"match_all": {}}

            client = self._http_client

            if True:
                resp = client.post(f"{self.url}/{self.index_name}/_search", json=query_body)
                if resp.status_code == 200:
                    data = resp.json()
                    total = data.get("hits", {}).get("total", {}).get("value", 0)
                    hits = [h.get("_source", {}) for h in data.get("hits", {}).get("hits", [])]
                    return {"total": total, "events": hits}
        except Exception:
            self._is_online = False

        return None

    def check_health(self) -> Dict[str, Any]:
        """Check OpenSearch cluster health and node status."""
        if self.is_available():
            try:
                client = self._http_client
                if True:
                    resp = client.get(f"{self.url}/_cluster/health")
                    if resp.status_code == 200:
                        data = resp.json()
                        cluster_status = data.get("status", "unknown")
                        return {
                            "status": "healthy" if cluster_status in ("green", "yellow") else cluster_status,
                            "cluster_name": data.get("cluster_name", "ulpf-cluster"),
                            "cluster_status": cluster_status,
                            "number_of_nodes": data.get("number_of_nodes", 1),
                            "active_shards": data.get("active_shards", 1),
                            "url": self.url,
                            "index": self.index_name,
                        }
            except Exception:
                self._is_online = False

        return {
            "status": "degraded (local fallback)",
            "url": self.url,
            "index": self.index_name,
            "error": "OpenSearch node offline; SQLite persistence active.",
        }
