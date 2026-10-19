"""
Configuration and settings for Task 1: The Knowledge Brain.
"""
import os
from pathlib import Path
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
ARTICLES_DIR = DATA_DIR / "articles"
SCREENSHOTS_DIR = DATA_DIR / "screenshots"
TICKETS_DIR = DATA_DIR / "tickets"
STATE_FILE = DATA_DIR / "sync_state.json"

for d in [DATA_DIR, ARTICLES_DIR, SCREENSHOTS_DIR, TICKETS_DIR]:
    d.mkdir(parents=True, exist_ok=True)


class Settings(BaseModel):
    app_name: str = "Knowledge Brain API"
    version: str = "1.0.0"
    host: str = os.getenv("KB_HOST", "0.0.0.0")
    port: int = int(os.getenv("KB_PORT", "8001"))
    sitemap_url: str = os.getenv(
        "SITEMAP_URL",
        "https://support.brilliantdirectories.com/support/sitemap.xml"
    )
    request_delay_seconds: float = float(os.getenv("SCRAPE_DELAY_SEC", "0.2"))
    max_scrape_batch: int = int(os.getenv("MAX_SCRAPE_BATCH", "25"))
    confidence_threshold: float = float(os.getenv("KB_CONFIDENCE_THRESHOLD", "0.45"))
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    default_model: str = os.getenv("KB_MODEL", "claude-3-5-sonnet-20241022")


settings = Settings()
