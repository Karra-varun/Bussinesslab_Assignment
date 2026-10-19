"""
Configuration for Task 3: Meeting to Scope of Work.
"""
import os
from pathlib import Path
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent.parent
TRANSCRIPTS_DIR = BASE_DIR / "app" / "transcripts"
TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)


class Settings(BaseModel):
    app_name: str = "Meeting-to-SOW Multi-Agent API"
    port: int = int(os.getenv("SOW_PORT", "8003"))
    host: str = os.getenv("SOW_HOST", "0.0.0.0")
    kb_api_url: str = os.getenv("KB_API_URL", "http://localhost:8001")
    developer_hourly_rate: float = float(os.getenv("HOURLY_RATE", "125.0"))
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")


settings = Settings()
