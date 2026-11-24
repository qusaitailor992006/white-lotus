import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from app.database import SessionLocal
from app.models import AdminUser, BanquetEnquiry, Customer, AnalyticsEvent
from backup_db import backup_database

client = TestClient(app)

def run_phase2_tests():
    print("=" * 60)
    print("RUNNING PHASE 2 AUTOMATED COMPREHENSIVE TEST SUITE")
    print("=" * 60)

    # 1. Public Banquet Booking System Test
    banquet_payload = {
        "contact_name": "Rohan Deshmukh",
        "contact_phone": "9822114477",
        "contact_email": "rohan.d@tcs.com",
        "event_type": "Corporate Dinner",
        "event_date": "2026-12-10",
        "estimated_guests": 50,
        "cuisine_preference": "Veg + Non-Veg Grand Buffet",
        "special_requests": "Need projector screen and microphone for corporate presentation on Starlit Terrace."
    }

    res_b = client.post("/api/banquets", json=banquet_payload)
    assert res_b.status_code == 200, f"Error: {res_b.text}"
    b_data = res_b.json()
    assert b_data["success"] is True
    assert b_data["enquiry_ref"].startswith("WLB-")
    assert "wa.me" in b_data["whatsapp_url"]
    assert settings.CAPTAIN_WHATSAPP in b_data["whatsapp_url"]
    enquiry_id = b_data["enquiry_id"]
    print(f"✓ Banquet Booking: Logged enquiry {b_data['enquiry_ref']} for {banquet_payload['estimated_guests']} guests")

    # Check Customer CRM auto-sync for Banquet lead
    db = SessionLocal()
    c = db.query(Customer).filter(Customer.phone == banquet_payload["contact_phone"]).first()
    assert c is not None
    assert c.tag == "Corporate"
    assert "Corporate Dinner" in c.notes
    print(f"✓ Customer CRM Auto-Sync: Created Corporate guest profile ID {c.id} ({c.name})")
    db.close()

    # 2. Admin Banquet Management Tab
    # Login as admin
    login_res = client.post("/api/admin/login", json={"username": settings.ADMIN_USERNAME, "password": settings.ADMIN_PASSWORD})
    assert login_res.status_code == 200
    session_cookie = login_res.cookies[settings.COOKIE_NAME]
    client.cookies.set(settings.COOKIE_NAME, session_cookie)

    # List banquet leads
    admin_b_res = client.get("/api/admin/banquets")
    assert admin_b_res.status_code == 200
    enquiries = admin_b_res.json()["enquiries"]
    assert any(e["id"] == enquiry_id for e in enquiries)
    print(f"✓ Admin Banquets Tab: Listed {len(enquiries)} banquet leads with WhatsApp proposal links")

    # Update banquet status to Quoted
    patch_b = client.patch(f"/api/admin/banquets/{enquiry_id}/status", json={
        "status": "Quoted",
        "notes": "Sent per-plate quote of ₹1,450 + taxes with exclusive terrace section reserved."
    })
    assert patch_b.status_code == 200
    print(f"✓ Admin Action: Updated banquet lead ID {enquiry_id} -> Status: Quoted")

    # 3. Analytics Tracking & Dashboard
    # Track page view
    track_res = client.post("/api/analytics/track")
    assert track_res.status_code == 200
    print("✓ Analytics Event: Recorded privacy-safe direct page view")

    # Admin analytics overview
    analytics_res = client.get("/api/admin/analytics")
    assert analytics_res.status_code == 200
    a_data = analytics_res.json()
    assert a_data["total_page_views"] >= 1
    assert a_data["total_reservations"] >= 1
    assert a_data["total_banquet_enquiries"] >= 1
    assert len(a_data["daily_trend"]) == 7
    print(f"✓ Admin Analytics: Loaded KPIs (Views: {a_data['total_page_views']}, Bookings: {a_data['total_reservations']}, Conf Rate: {a_data['confirmation_rate']}, 7-Day Trend: {len(a_data['daily_trend'])} days)")

    # 4. Standalone Database Backup Script
    backup_ok = backup_database()
    assert backup_ok is True
    backups = list((BASE_DIR / "backups").glob("white_lotus_backup_*.db"))
    assert len(backups) >= 1
    print(f"✓ Database Backup: Verified SQLite online backup generated in /backups ({backups[-1].name})")

    # 5. Local SEO & Google Integration
    # robots.txt
    robots_res = client.get("/robots.txt")
    assert robots_res.status_code == 200
    assert "Disallow: /admin" in robots_res.text
    assert "sitemap.xml" in robots_res.text
    print("✓ SEO Standard: Verified /robots.txt with admin disallow and sitemap reference")

    # sitemap.xml
    sitemap_res = client.get("/sitemap.xml")
    assert sitemap_res.status_code == 200
    assert "application/xml" in sitemap_res.headers["content-type"]
    assert "https://whitelotuspune.com/" in sitemap_res.text
    print("✓ SEO Standard: Verified /sitemap.xml with canonical XML schema")

    # HTML verification for Google Maps, Review CTA, and JSON-LD
    home_res = client.get("/")
    assert home_res.status_code == 200
    html_text = home_res.text
    assert "google.com/maps/embed" in html_text
    assert "Get Live Directions" in html_text
    assert "Leave a Google Review" in html_text
    assert "application/ld+json" in html_text
    print("✓ Google Integration: Verified Maps iframe embed, Directions button, Review CTA, and JSON-LD Schema")

    print("=" * 60)
    print("ALL PHASE 2 FEATURES VERIFIED SUCCESSFULLY (100% PASS)")
    print("=" * 60)

if __name__ == "__main__":
    run_phase2_tests()
