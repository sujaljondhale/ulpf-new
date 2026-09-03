from typing import Optional
from pydantic import BaseModel, Field


class Settings(BaseModel):
    app_name: str = "Universal Log Pre-processing Framework (ULPF)"
    version: str = "1.0.0"
    schema_version: str = "1.0"
    environment: str = "development"
    debug: bool = True
    
    # Payload limits & security
    max_log_payload_bytes: int = 10 * 1024 * 1024  # 10 MB limit
    rate_limit_per_minute: int = 6000
    
    # Local AI / Ollama Configuration
    ollama_host: str = "http://localhost:11434"
    ai_model_name: str = "qwen2.5-coder:3b"
    ai_enabled: bool = True
    ai_confidence_threshold: float = 0.80

    # Persistence & Exporters
    storage_dir: str = "storage/raw"
    db_sqlite_path: str = "storage/ulpf_metadata.db"


settings = Settings()
