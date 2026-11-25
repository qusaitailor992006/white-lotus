import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Fallback parser for .env without complex dependencies
def load_dotenv_simple():
    env_file = BASE_DIR / ".env"
    if env_file.exists():
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    k = k.strip()
                    v = v.strip().strip("'\"")
                    if k not in os.environ:
                        os.environ[k] = v

load_dotenv_simple()

class Settings:
    PROJECT_NAME: str = "White Lotus: Food Vibe Folks"
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'white_lotus.db'}")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "whitelotus-pune-luxury-secret-key-2026-sarasbaug")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    ADMIN_USERNAME: str = os.getenv("ADMIN_USERNAME", "lotus_admin")
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "Lotus@Pune2026!")
    CAPTAIN_WHATSAPP: str = os.getenv("CAPTAIN_WHATSAPP", "919513575757")
    COOKIE_NAME: str = "whitelotus_admin_session"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "production")
    ENABLE_DOCS: bool = os.getenv("ENABLE_DOCS", "false").lower() in ("true", "1")
    
    # Strict CORS Allowlist (Audit 6.2 - No wildcard with credentials)
    ALLOWED_ORIGINS: list = [
        "https://whitelotuspune.com",
        "https://www.whitelotuspune.com",
        "https://qusaitailor992006.github.io",
        "http://127.0.0.1:8000",
        "http://localhost:8000",
    ]
    
    # Official Business Details (Legal Compliance)
    BUSINESS_NAME: str = "White Lotus: Food Vibe Folks"
    BUSINESS_ADDRESS: str = "202, 203 Saras Baug Road, Opposite Sanas Ground, Parvati, Pune 411009, Maharashtra, India"
    BUSINESS_PHONE: str = "+91 95135 75757"
    BUSINESS_EMAIL: str = "concierge@whitelotuspune.com"
    GSTIN: str = "27AAACW8921M1ZX"
    FSSAI_NO: str = "11523034000492"

settings = Settings()
