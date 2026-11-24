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

settings = Settings()
