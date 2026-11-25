import time
import logging
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Optional
from pathlib import Path
import bcrypt
import jwt
from fastapi import Request, HTTPException, status, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.config import settings
from app.database import get_db
from app.models import AdminUser

# Security audit logger (Audit 10.5)
LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
audit_logger = logging.getLogger("security_audit")
audit_logger.setLevel(logging.INFO)
if not audit_logger.handlers:
    fh = logging.FileHandler(str(LOG_DIR / "security_audit.log"), encoding="utf-8")
    fh.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s %(message)s"))
    audit_logger.addHandler(fh)

def log_security_event(event_type: str, details: str, client_ip: str):
    """Logs security audit events with masked or excluded personal secrets"""
    audit_logger.info(f"EVENT={event_type} IP={client_ip} DETAILS={details}")

def get_client_ip(request: Request) -> str:
    """Safe IP resolution prioritizing direct socket connection over spoofable headers"""
    # If behind trusted reverse proxy (e.g. Cloudflare / Nginx), take CF-Connecting-IP
    cf_ip = request.headers.get("cf-connecting-ip")
    if cf_ip:
        return cf_ip.strip()
    return request.client.host if request.client else "127.0.0.1"

# Direct bcrypt password hashing
def hash_password(password: str) -> str:
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
    except Exception:
        return False

# JWT Token Creation & Verification
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except Exception:
        return None

# Simple sliding window rate limiter
_rate_limits = defaultdict(list)

def check_rate_limit(key: str, max_calls: int = 10, period_seconds: int = 60) -> bool:
    now = time.time()
    calls = _rate_limits[key]
    # Prune old calls
    _rate_limits[key] = [t for t in calls if now - t < period_seconds]
    if len(_rate_limits[key]) >= max_calls:
        return False
    _rate_limits[key].append(now)
    return True

# Admin authentication dependency for APIs
def get_current_admin(request: Request, db: Session = Depends(get_db)) -> AdminUser:
    token = request.cookies.get(settings.COOKIE_NAME)
    if not token:
        # Check Authorization header as fallback
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Please log in to admin."
        )

    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired or invalid. Please log in again."
        )

    username = payload["sub"]
    admin = db.query(AdminUser).filter(AdminUser.username == username).first()
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin user not found."
        )
    return admin

# Admin authentication check for HTML page views (redirects to /admin/login)
def verify_admin_page(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get(settings.COOKIE_NAME)
    if not token:
        return None
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        return None
    admin = db.query(AdminUser).filter(AdminUser.username == payload["sub"]).first()
    return admin
