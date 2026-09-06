import os
from typing import Optional
from pydantic import BaseModel, Field


class Settings(BaseModel):
    app_name: str = "Universal Log Pre-processing Framework (ULPF)"
    version: str = "1.0.0"
    schema_version: str = "1.0"
    environment: str = Field(default_factory=lambda: os.getenv("ULPF_ENV", "development"))
    debug: bool = Field(default_factory=lambda: os.getenv("ULPF_DEBUG", "false").lower() in ("true", "1", "yes"))

    # API Server Configuration
    api_host: str = Field(default_factory=lambda: os.getenv("ULPF_API_HOST", "0.0.0.0"))
    api_port: int = Field(default_factory=lambda: int(os.getenv("ULPF_API_PORT", "8000")))

    # Syslog UDP Collector Configuration
    syslog_udp_enabled: bool = Field(default_factory=lambda: os.getenv("SYSLOG_UDP_ENABLED", "true").lower() in ("true", "1", "yes"))
    syslog_udp_host: str = Field(default_factory=lambda: os.getenv("SYSLOG_UDP_HOST", "0.0.0.0"))
    syslog_udp_port: int = Field(default_factory=lambda: int(os.getenv("SYSLOG_UDP_PORT", "5140")))

    # Syslog TCP Collector Configuration
    syslog_tcp_enabled: bool = Field(default_factory=lambda: os.getenv("SYSLOG_TCP_ENABLED", "true").lower() in ("true", "1", "yes"))
    syslog_tcp_host: str = Field(default_factory=lambda: os.getenv("SYSLOG_TCP_HOST", "0.0.0.0"))
    syslog_tcp_port: int = Field(default_factory=lambda: int(os.getenv("SYSLOG_TCP_PORT", "5141")))

    # Syslog TLS Architecture
    syslog_tls_enabled: bool = Field(default_factory=lambda: os.getenv("SYSLOG_TLS_ENABLED", "false").lower() in ("true", "1", "yes"))
    syslog_tls_port: int = Field(default_factory=lambda: int(os.getenv("SYSLOG_TLS_PORT", "6514")))
    syslog_tls_certfile: Optional[str] = Field(default_factory=lambda: os.getenv("SYSLOG_TLS_CERTFILE", None))
    syslog_tls_keyfile: Optional[str] = Field(default_factory=lambda: os.getenv("SYSLOG_TLS_KEYFILE", None))

    # File Tail Collector Configuration
    file_collector_enabled: bool = Field(default_factory=lambda: os.getenv("FILE_COLLECTOR_ENABLED", "true").lower() in ("true", "1", "yes"))
    file_watch_dir: str = Field(default_factory=lambda: os.getenv("FILE_WATCH_DIR", "storage/logs"))

    # Ingestion Buffer & Rate Limiting
    max_log_payload_bytes: int = 10 * 1024 * 1024  # 10 MB limit
    rate_limit_per_minute: int = 6000
    max_events_per_second: int = Field(default_factory=lambda: int(os.getenv("MAX_EVENTS_PER_SECOND", "25000")))
    ingress_queue_max_size: int = Field(default_factory=lambda: int(os.getenv("INGRESS_QUEUE_MAX_SIZE", "50000")))

    # Local AI / Ollama Configuration
    ollama_host: str = Field(
        default_factory=lambda: os.getenv("OLLAMA_URL", os.getenv("OLLAMA_HOST", "http://localhost:11434"))
    )
    ai_model_name: str = Field(
        default_factory=lambda: os.getenv("OLLAMA_MODEL", os.getenv("AI_MODEL_NAME", "qwen2.5-coder:3b"))
    )
    ai_enabled: bool = Field(
        default_factory=lambda: os.getenv("AI_ENABLED", "true").lower() in ("true", "1", "yes")
    )
    ai_confidence_threshold: float = 0.80

    # MinIO / S3 Raw Evidence Storage Configuration
    minio_endpoint: str = Field(
        default_factory=lambda: os.getenv("MINIO_ENDPOINT", os.getenv("MINIO_HOST", "minio:9000"))
    )
    minio_access_key: str = Field(
        default_factory=lambda: os.getenv("MINIO_ACCESS_KEY", os.getenv("MINIO_ROOT_USER", "ulpf_admin"))
    )
    minio_secret_key: str = Field(
        default_factory=lambda: os.getenv("MINIO_SECRET_KEY", os.getenv("MINIO_ROOT_PASSWORD", "ulpf_password_2026"))
    )
    minio_bucket: str = Field(
        default_factory=lambda: os.getenv("MINIO_BUCKET", "ulpf-raw")
    )
    minio_secure: bool = Field(
        default_factory=lambda: os.getenv("MINIO_SECURE", "false").lower() in ("true", "1", "yes")
    )

    # OpenSearch Searchable Representation Configuration
    opensearch_url: str = Field(
        default_factory=lambda: os.getenv("OPENSEARCH_URL", os.getenv("OPENSEARCH_HOST", "http://opensearch:9200"))
    )
    opensearch_index: str = Field(
        default_factory=lambda: os.getenv("OPENSEARCH_INDEX", "ulpf-events")
    )

    # Persistence & SQLite Database
    storage_dir: str = Field(
        default_factory=lambda: os.getenv("STORAGE_DIR", "storage/raw")
    )
    db_sqlite_path: str = Field(
        default_factory=lambda: os.getenv("DB_SQLITE_PATH", "storage/ulpf_metadata.db")
    )


settings = Settings()
