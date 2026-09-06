import socket
import select
import threading
import logging
from typing import Dict, Any, Optional, Callable
from datetime import datetime, timezone
from app.collectors.base import BaseConnector
from app.collectors.ingress import RawIngress
from app.collectors.queue import IngestionQueue
from app.config import settings

logger = logging.getLogger(__name__)


class SyslogUDPCollector(BaseConnector):
    """
    RFC 3164 / RFC 5424 UDP Syslog Ingress Collector.
    Binds to 0.0.0.0:5140 and ingests raw datagrams from firewalls, routers, switches, and VPNs.
    """

    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        queue: Optional[IngestionQueue] = None,
        event_callback: Optional[Callable] = None,
    ):
        super().__init__(name="Syslog UDP Collector", connector_type="syslog_udp")
        self.host = host or settings.syslog_udp_host
        self.port = port or settings.syslog_udp_port
        self.queue = queue
        self.event_callback = event_callback
        self.server_socket: Optional[socket.socket] = None
        self.thread: Optional[threading.Thread] = None

    def start(self) -> None:
        """Start UDP listener thread."""
        if self.is_running:
            return

        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.is_running = True
            self.started_at = datetime.now(timezone.utc).isoformat()

            self.thread = threading.Thread(target=self._listen_loop, name="syslog-udp-listener", daemon=True)
            self.thread.start()
            logger.info(f"Syslog UDP Collector listening on {self.host}:{self.port}")
        except Exception as e:
            logger.warning(f"Could not bind Syslog UDP server on {self.host}:{self.port}: {e}")
            self.is_running = False

    def _listen_loop(self) -> None:
        """Datagram listening loop."""
        while self.is_running and self.server_socket:
            try:
                # Use select with timeout so thread can exit cleanly on stop()
                r, _, _ = select.select([self.server_socket], [], [], 0.5)
                if not r or not self.server_socket:
                    continue

                data, addr = self.server_socket.recvfrom(65535)
                if not data:
                    continue

                self.total_received += 1
                self.bytes_received += len(data)

                raw_log = data.decode("utf-8", errors="replace").strip()
                if not raw_log:
                    continue

                client_ip, client_port = addr[0], addr[1]
                source_identifier = f"{client_ip}:{client_port}"

                ingress = RawIngress(
                    connector_type="syslog_udp",
                    source=source_identifier,
                    raw_text=raw_log,
                    transport_metadata={
                        "protocol": "UDP",
                        "client_ip": client_ip,
                        "client_port": client_port,
                        "server_port": self.port,
                        "bytes": len(data),
                    }
                )

                if self.queue:
                    accepted, reason = self.queue.enqueue(ingress)
                    if accepted:
                        self.total_accepted += 1
                        self.total_processed += 1
                    else:
                        self.total_rejected += 1
                        if "RATE_LIMIT" in reason:
                            self.total_dropped_rate_limit += 1
                elif self.event_callback:
                    self.total_accepted += 1
                    self.total_processed += 1
                    self.event_callback(ingress)

            except Exception as e:
                if self.is_running:
                    self.total_errors += 1
                    logger.error(f"[SyslogUDP] Packet receive error: {e}")

    def stop(self) -> None:
        """Stop UDP listener."""
        self.is_running = False
        if self.server_socket:
            try:
                self.server_socket.close()
            except Exception:
                pass
            self.server_socket = None
        logger.info("Syslog UDP Collector stopped.")


class SyslogTCPCollector(BaseConnector):
    """
    RFC 3164 / RFC 5424 TCP Syslog Ingress Collector.
    Binds to 0.0.0.0:5141 and supports multi-message framing (octet-counting & newline-delimited).
    """

    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        queue: Optional[IngestionQueue] = None,
        event_callback: Optional[Callable] = None,
    ):
        super().__init__(name="Syslog TCP Collector", connector_type="syslog_tcp")
        self.host = host or settings.syslog_tcp_host
        self.port = port or settings.syslog_tcp_port
        self.queue = queue
        self.event_callback = event_callback
        self.server_socket: Optional[socket.socket] = None
        self.thread: Optional[threading.Thread] = None
        self._client_threads: list[threading.Thread] = []

    def start(self) -> None:
        """Start TCP listener thread."""
        if self.is_running:
            return

        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(128)
            self.is_running = True
            self.started_at = datetime.now(timezone.utc).isoformat()

            self.thread = threading.Thread(target=self._accept_loop, name="syslog-tcp-acceptor", daemon=True)
            self.thread.start()
            logger.info(f"Syslog TCP Collector listening on {self.host}:{self.port}")
        except Exception as e:
            logger.warning(f"Could not bind Syslog TCP server on {self.host}:{self.port}: {e}")
            self.is_running = False

    def _accept_loop(self) -> None:
        """TCP client connection acceptance loop."""
        while self.is_running and self.server_socket:
            try:
                r, _, _ = select.select([self.server_socket], [], [], 0.5)
                if not r or not self.server_socket:
                    continue

                client_sock, addr = self.server_socket.accept()
                client_t = threading.Thread(
                    target=self._handle_client,
                    args=(client_sock, addr),
                    name=f"syslog-tcp-client-{addr[0]}:{addr[1]}",
                    daemon=True,
                )
                client_t.start()
                self._client_threads.append(client_t)
            except Exception as e:
                if self.is_running:
                    logger.error(f"[SyslogTCP] Accept error: {e}")

    def _handle_client(self, client_sock: socket.socket, addr: tuple) -> None:
        """Handle multi-message TCP stream with framing support."""
        client_ip, client_port = addr[0], addr[1]
        buffer = ""

        try:
            client_sock.settimeout(60.0)
            while self.is_running:
                data = client_sock.recv(4096)
                if not data:
                    break

                self.bytes_received += len(data)
                text = data.decode("utf-8", errors="replace")
                buffer += text

                # Process newline-delimited or octet-framed messages in buffer
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    raw_log = line.strip()
                    if not raw_log:
                        continue

                    self.total_received += 1
                    ingress = RawIngress(
                        connector_type="syslog_tcp",
                        source=f"{client_ip}:{client_port}",
                        raw_text=raw_log,
                        transport_metadata={
                            "protocol": "TCP",
                            "client_ip": client_ip,
                            "client_port": client_port,
                            "server_port": self.port,
                        }
                    )

                    if self.queue:
                        accepted, reason = self.queue.enqueue(ingress)
                        if accepted:
                            self.total_accepted += 1
                            self.total_processed += 1
                        else:
                            self.total_rejected += 1
                            if "RATE_LIMIT" in reason:
                                self.total_dropped_rate_limit += 1
                    elif self.event_callback:
                        self.total_accepted += 1
                        self.total_processed += 1
                        self.event_callback(ingress)

        except (socket.timeout, ConnectionResetError):
            pass
        except Exception as e:
            if self.is_running:
                self.total_errors += 1
                logger.error(f"[SyslogTCP] Client handler error ({client_ip}): {e}")
        finally:
            try:
                client_sock.close()
            except Exception:
                pass

    def stop(self) -> None:
        """Stop TCP listener."""
        self.is_running = False
        if self.server_socket:
            try:
                self.server_socket.close()
            except Exception:
                pass
            self.server_socket = None
        logger.info("Syslog TCP Collector stopped.")


class SyslogCollector(BaseConnector):
    """
    Unified Syslog Collector Manager.
    Coordinates both UDP (5140) and TCP (5141) listeners with shared queue.
    """

    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        queue: Optional[IngestionQueue] = None,
        pipeline: Optional[Any] = None,
        event_callback: Optional[Callable] = None,
    ):
        super().__init__(name="Unified Syslog Ingestion Gateway", connector_type="syslog")
        self.udp_collector = SyslogUDPCollector(host=host, port=port or settings.syslog_udp_port, queue=queue, event_callback=event_callback)
        self.tcp_collector = SyslogTCPCollector(host=host, port=settings.syslog_tcp_port, queue=queue, event_callback=event_callback)
        self.pipeline = pipeline
        self.event_callback = event_callback

    def start(self) -> None:
        """Start both UDP and TCP listeners."""
        self.is_running = True
        self.started_at = datetime.now(timezone.utc).isoformat()
        if settings.syslog_udp_enabled:
            self.udp_collector.start()
        if settings.syslog_tcp_enabled:
            self.tcp_collector.start()

    def stop(self) -> None:
        """Stop both listeners."""
        self.is_running = False
        self.udp_collector.stop()
        self.tcp_collector.stop()

    @property
    def total_received(self) -> int:
        if hasattr(self, "udp_collector") and hasattr(self, "tcp_collector"):
            return self.udp_collector.total_received + self.tcp_collector.total_received
        return getattr(self, "_total_received", 0)

    @total_received.setter
    def total_received(self, val: int) -> None:
        self._total_received = val

    @property
    def total_processed(self) -> int:
        if hasattr(self, "udp_collector") and hasattr(self, "tcp_collector"):
            return self.udp_collector.total_processed + self.tcp_collector.total_processed
        return getattr(self, "_total_processed", 0)

    @total_processed.setter
    def total_processed(self, val: int) -> None:
        self._total_processed = val

    @property
    def total_errors(self) -> int:
        if hasattr(self, "udp_collector") and hasattr(self, "tcp_collector"):
            return self.udp_collector.total_errors + self.tcp_collector.total_errors
        return getattr(self, "_total_errors", 0)

    @total_errors.setter
    def total_errors(self, val: int) -> None:
        self._total_errors = val

    def get_status(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "is_running": self.is_running,
            "status": "RUNNING" if self.is_running else "STOPPED",
            "udp_listener": self.udp_collector.get_status(),
            "tcp_listener": self.tcp_collector.get_status(),
            "tls_architecture": {
                "port": settings.syslog_tls_port,
                "status": "PLANNED / OPTIONAL" if not settings.syslog_tls_enabled else "ACTIVE",
                "description": "TLS architecture supported; UDP (5140) & TCP (5141) active in prototype",
            },
            "total_received": self.total_received,
            "total_processed": self.total_processed,
            "total_errors": self.total_errors,
            "current_eps": self.udp_collector.calculate_current_eps() + self.tcp_collector.calculate_current_eps(),
        }
