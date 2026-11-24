import os
from pathlib import Path
from fastapi import FastAPI, Request, Depends, status, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, PlainTextResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.config import settings, BASE_DIR
from app.database import get_db, engine, Base
from app.seed import seed_database
from app.security import verify_admin_page
from app.routers import public, admin

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Luxury Fine Dining Web Platform & Operational CRM Engine",
    version="2.0.0"
)

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
    <lastmod>2026-11-24</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://whitelotuspune.com/#dining-experience</loc>
    <lastmod>2026-11-24</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://whitelotuspune.com/#culinary-menu</loc>
    <lastmod>2026-11-24</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://whitelotuspune.com/#vip-reservations</loc>
    <lastmod>2026-11-24</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.9</priority>
  </url>
</urlset>"""
    return Response(content=xml_content, media_type="application/xml")
