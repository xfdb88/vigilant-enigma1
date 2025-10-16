import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    ig_user: str = os.getenv("IG_USERNAME", "")
    ig_pass: str = os.getenv("IG_PASSWORD", "")
    proxy: str | None = os.getenv("PROXY_URL") or None
    headless: bool = os.getenv("HEADLESS", "true").lower() == "true"
    qps: float = float(os.getenv("RATE_LIMIT_QPS", "0.3"))
    retry_attempts: int = int(os.getenv("RETRY_ATTEMPTS", "3"))
    retry_backoff: float = float(os.getenv("RETRY_BACKOFF", "2"))
    timeout: float = float(os.getenv("TIMEOUT_SECONDS", "30"))
