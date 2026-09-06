import time
import queue
import threading
import logging
from typing import Optional, Callable, Dict, Any, Tuple
from app.collectors.ingress import RawIngress
from app.config import settings

logger = logging.getLogger(__name__)


class IngestionQueue:
    """
    High-Throughput Ingestion Queue & Backpressure Controller.
    Buffers raw log items from network/file/REST connectors, applies rate limiting,
    and feeds pipeline worker threads with non-blocking backpressure protection.
    """

    def __init__(
        self,
        max_size: Optional[int] = None,
        max_eps: Optional[int] = None,
        worker_count: int = 2,
        pipeline: Optional[Any] = None,
        event_callback: Optional[Callable] = None,
    ):
        self.max_size = max_size or settings.ingress_queue_max_size
        self.max_eps = max_eps or settings.max_events_per_second
        self.worker_count = worker_count
        self.pipeline = pipeline
        self.event_callback = event_callback

        self._queue: queue.Queue = queue.Queue(maxsize=self.max_size)
        self._is_running = False
        self._workers: list[threading.Thread] = []

        # Metrics
        self.total_enqueued = 0
        self.total_processed = 0
        self.total_dropped_rate_limit = 0
        self.total_dropped_backpressure = 0
        self.total_errors = 0

        # Rate limiter sliding window
        self._window_start = time.time()
        self._window_count = 0
        self._rate_lock = threading.Lock()

    def start(self) -> None:
        """Start worker threads consuming from queue."""
        if self._is_running:
            return

        self._is_running = True
        self._workers = []
        for i in range(self.worker_count):
            t = threading.Thread(target=self._worker_loop, name=f"ulpf-worker-{i+1}", daemon=True)
            t.start()
            self._workers.append(t)
        logger.info(f"IngestionQueue started with {self.worker_count} workers (max_size={self.max_size}, max_eps={self.max_eps}).")

    def stop(self) -> None:
        """Stop worker threads."""
        self._is_running = False
        for _ in range(self.worker_count):
            try:
                self._queue.put_nowait(None)
            except Exception:
                pass
        logger.info("IngestionQueue stopped.")

    def _check_rate_limit(self) -> bool:
        """Sliding window rate limit check."""
        now = time.time()
        with self._rate_lock:
            if now - self._window_start >= 1.0:
                self._window_start = now
                self._window_count = 0

            if self._window_count >= self.max_eps:
                return False

            self._window_count += 1
            return True

    def enqueue(self, ingress: RawIngress) -> Tuple[bool, str]:
        """
        Non-blocking enqueue with rate limiting and backpressure protection.
        Returns (accepted: bool, reason: str).
        """
        # 1. Rate Limit Check
        if not self._check_rate_limit():
            self.total_dropped_rate_limit += 1
            return False, "RATE_LIMIT_EXCEEDED"

        # 2. Queue Capacity & Backpressure Check
        try:
            self._queue.put_nowait(ingress)
            self.total_enqueued += 1
            return True, "ACCEPTED"
        except queue.Full:
            self.total_dropped_backpressure += 1
            return False, "QUEUE_FULL_BACKPRESSURE"

    def _worker_loop(self) -> None:
        """Worker loop processing enqueued RawIngress objects."""
        while self._is_running:
            try:
                item = self._queue.get(timeout=0.5)
                if item is None:
                    break

                try:
                    if self.pipeline:
                        # Process raw text through ULPF pipeline
                        ir_event = self.pipeline.process(
                            raw_message=item.raw_text,
                            source=item.source,
                        )

                        # Attach ingress transport metadata to original log metadata if present
                        if hasattr(ir_event, "original") and item.transport_metadata:
                            setattr(ir_event.original, "transport", item.connector_type)

                        if self.event_callback:
                            self.event_callback(ir_event, source_name=item.source)

                    self.total_processed += 1
                except Exception as e:
                    self.total_errors += 1
                    logger.error(f"[IngestionQueue] Processing error: {e}")
                finally:
                    self._queue.task_done()
            except queue.Empty:
                continue
            except Exception:
                pass

    def get_metrics(self) -> Dict[str, Any]:
        """Return real-time queue depth and performance metrics."""
        return {
            "queue_depth": self._queue.qsize(),
            "max_queue_size": self.max_size,
            "max_eps_limit": self.max_eps,
            "worker_threads": len(self._workers),
            "is_running": self._is_running,
            "total_enqueued": self.total_enqueued,
            "total_processed": self.total_processed,
            "total_dropped_rate_limit": self.total_dropped_rate_limit,
            "total_dropped_backpressure": self.total_dropped_backpressure,
            "total_errors": self.total_errors,
        }
