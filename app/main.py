import os
from pathlib import Path
from fastapi import FastAPI, Request, Depends, status, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, PlainTextResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import Session

from app.config import settings, BASE_DIR
from app.database import get_db, engine, Base
from app.seed import seed_database
from app.security import verify_admin_page, log_security_event, get_client_ip
from app.routers import public, admin

# Audit 10.3: Protect or disable FastAPI docs in production
docs_url = "/docs" if settings.ENABLE_DOCS or settings.ENVIRONMENT == "development" else None
redoc_url = "/redoc" if settings.ENABLE_DOCS or settings.ENVIRONMENT == "development" else None
openapi_url = "/openapi.json" if settings.ENABLE_DOCS or settings.ENVIRONMENT == "development" else None

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Luxury Fine Dining Web Platform & Operational CRM Engine",
    version="2.0.0",
    docs_url=docs_url,
    redoc_url=redoc_url,
    openapi_url=openapi_url
)

# Audit 6.2: Strict CORS allowlist (Never allow_origins=['*'] with allow_credentials=True)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Audit 10.1 & 10.4: Security Headers & Sensitive File Shield Middleware
class SecurityShieldMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path.lower()
        client_ip = get_client_ip(request)

        # Check 10.4: Block attempts to probe sensitive files (.env, .git, backups, database dumps)
        if any(bad in path for bad in [".env", ".git", ".db", ".sqlite", "backup", "dump", ".sql"]):
            log_security_event("PROBE_BLOCKED", f"Attempted access to sensitive path: {path}", client_ip)
            return PlainTextResponse("Access Denied", status_code=403)

        response = await call_next(request)

        # Check 10.1: Set industry standard HTTP security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), camera=(), microphone=()"
        response.headers["X-XSS-Protection"] = "1; mode=block"

        return response

app.add_middleware(SecurityShieldMiddleware)

# Setup Templates & Static directories
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

STATIC_DIR.mkdir(parents=True, exist_ok=True)
(BASE_DIR / "backups").mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Include Routers
app.include_router(public.router)
app.include_router(admin.router)

# Automatic database initialization & seed on startup
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    seed_database()

# --- WEB PAGE ROUTES ---

@app.get("/", response_class=HTMLResponse)
def home_page(request: Request):
    """Public luxury landing page with 3D petals, dynamic menu & reservation desk"""
    index_file = TEMPLATES_DIR / "index.html"
    if not index_file.exists():
        root_index = BASE_DIR / "index.html"
        if root_index.exists():
            return HTMLResponse(content=root_index.read_text(encoding="utf-8"))
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/admin/login", response_class=HTMLResponse)
def admin_login_page(request: Request, db: Session = Depends(get_db)):
    """Admin staff login page; redirects to dashboard if already authenticated"""
    current_admin = verify_admin_page(request, db)
    if current_admin:
        return RedirectResponse(url="/admin", status_code=status.HTTP_303_SEE_OTHER)
    return templates.TemplateResponse(request=request, name="admin_login.html")

@app.get("/admin", response_class=HTMLResponse)
def admin_dashboard_page(request: Request, db: Session = Depends(get_db)):
    """Protected executive management dashboard; redirects to /admin/login if not authenticated"""
    current_admin = verify_admin_page(request, db)
    if not current_admin:
        return RedirectResponse(url="/admin/login", status_code=status.HTTP_303_SEE_OTHER)
    return templates.TemplateResponse(
        request=request,
        name="admin_dashboard.html",
        context={"admin": current_admin}
    )

# --- LEGAL & COMPLIANCE PAGES (The 20 "Don't Get Sued" Protections) ---

@app.get("/privacy", response_class=HTMLResponse)
def privacy_policy_page(request: Request):
    """DPDP Act 2023 & IT Act compliant Privacy Policy"""
    return templates.TemplateResponse(request=request, name="privacy_policy.html")

@app.get("/terms", response_class=HTMLResponse)
def terms_of_service_page(request: Request):
    """Terms of Service covering table bookings, etiquette & cancellation terms"""
    return templates.TemplateResponse(request=request, name="terms_of_service.html")

@app.get("/refunds", response_class=HTMLResponse)
def refund_policy_page(request: Request):
    """Transparent zero hidden fee dining & banquet cancellation terms"""
    return templates.TemplateResponse(request=request, name="refund_policy.html")

@app.get("/cookie-policy", response_class=HTMLResponse)
def cookie_policy_page(request: Request):
    """Essential cookie usage & privacy declaration"""
    return templates.TemplateResponse(request=request, name="cookie_policy.html")

# --- SEO & CRAWLER ROUTES ---

@app.get("/robots.txt", response_class=PlainTextResponse)
def robots_txt():
    return (
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /admin\n"
        "Disallow: /admin/*\n"
        "Disallow: /api/admin/*\n"
        "Sitemap: https://whitelotuspune.com/sitemap.xml\n"
    )

@app.get("/sitemap.xml")
def sitemap_xml():
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://whitelotuspune.com/</loc>
    <lastmod>2026-11-25</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://whitelotuspune.com/#dining-experience</loc>
    <lastmod>2026-11-25</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://whitelotuspune.com/#culinary-menu</loc>
    <lastmod>2026-11-25</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://whitelotuspune.com/#vip-reservations</loc>
    <lastmod>2026-11-25</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://whitelotuspune.com/privacy</loc>
    <lastmod>2026-11-25</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.5</priority>
  </url>
  <url>
    <loc>https://whitelotuspune.com/terms</loc>
    <lastmod>2026-11-25</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.5</priority>
  </url>
</urlset>"""
    return Response(content=xml_content, media_type="application/xml")
