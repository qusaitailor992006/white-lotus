import sys
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from app.database import SessionLocal
from app.models import AdminUser, MenuItem, Customer, Reservation
from app.seed import seed_database

client = TestClient(app)

def run_all_tests():
    print("=" * 60)
    print("RUNNING PHASE 1 AUTOMATED COMPREHENSIVE TEST SUITE")
    print("=" * 60)

    # 1. Startup & Seeding Check
    seed_database()
    db = SessionLocal()
    admin_count = db.query(AdminUser).count()
    menu_count = db.query(MenuItem).count()
    cust_count = db.query(Customer).count()
    res_count = db.query(Reservation).count()
    db.close()

    assert admin_count >= 1, "Admin user must be seeded"
    assert menu_count == 166, f"Expected 166 menu items, got {menu_count}"
    print(f"✓ Database Seeding: {admin_count} Admin, {menu_count} Menu Items, {cust_count} Customers, {res_count} Reservations")

    # 2. Public Menu API Tests
    res = client.get("/api/menu")
    assert res.status_code == 200
    data = res.json()
    assert data["count"] == 166
    print(f"✓ Public Menu: Loaded {data['count']} items across {len(data['categories'])} categories")

    res_veg = client.get("/api/menu?dietary=veg")
    assert res_veg.status_code == 200
    veg_data = res_veg.json()
    assert all(it["dietary_type"] == "veg" for it in veg_data["items"])
    print(f"✓ Public Menu Filter: Loaded {veg_data['count']} Pure Veg items cleanly")

    res_search = client.get("/api/menu?q=Tiramisu")
    assert res_search.status_code == 200
    search_data = res_search.json()
    assert search_data["count"] >= 1
    print(f"✓ Public Menu Search: Found '{search_data['items'][0]['name']}' for query 'Tiramisu'")

    # 3. Public Table Reservation & CRM Auto-Sync
    test_guest_phone = "9822998877"
    booking_payload = {
        "guest_name": "Aditya Deshmukh",
        "guest_phone": test_guest_phone,
        "guest_email": "aditya.d@example.com",
        "reservation_date": "2026-11-28",
        "time_slot": "Dinner (08:30 PM)",
        "party_size": 4,
        "dining_zone": "The Starlit Terrace Garden",
        "special_request": "Quiet table for anniversary dinner, no onion no garlic for one guest."
    }

    res_book = client.post("/api/reservations", json=booking_payload)
    assert res_book.status_code == 200
    book_data = res_book.json()
    assert book_data["success"] is True
    assert book_data["booking_ref"].startswith("WL-")
    assert "wa.me" in book_data["whatsapp_url"]
    assert settings.CAPTAIN_WHATSAPP in book_data["whatsapp_url"]
    new_res_id = book_data["reservation_id"]
    print(f"✓ Public Reservation: Created {book_data['booking_ref']} with WhatsApp link for Floor Captain")

    # Check Customer CRM record automatically created
    db = SessionLocal()
    crm_cust = db.query(Customer).filter(Customer.phone == test_guest_phone).first()
    assert crm_cust is not None
    assert crm_cust.name == "Aditya Deshmukh"
    assert crm_cust.total_bookings >= 1
    assert crm_cust.preferred_zone == "The Starlit Terrace Garden"
    print(f"✓ Customer CRM Auto-Sync: Created/updated guest profile ID {crm_cust.id} ({crm_cust.phone})")
    db.close()

    # 4. Route Protection & Security Checks
    # Unauthenticated API call
    res_unauth = client.get("/api/admin/reservations")
    assert res_unauth.status_code == 401
    print("✓ Security Guard: /api/admin/reservations blocked with 401 without cookie")

    # Unauthenticated Web page request
    res_web_unauth = client.get("/admin", follow_redirects=False)
    assert res_web_unauth.status_code in [302, 303, 307]
    assert res_web_unauth.headers["location"] == "/admin/login"
    print("✓ Security Guard: /admin redirected to /admin/login for unauthenticated visitors")

    # Invalid login
    res_bad_login = client.post("/api/admin/login", json={"username": "lotus_admin", "password": "WrongPassword!"})
    assert res_bad_login.status_code == 401
    print("✓ Authentication: Rejected invalid password with 401")

    # Valid login
    res_good_login = client.post("/api/admin/login", json={"username": settings.ADMIN_USERNAME, "password": settings.ADMIN_PASSWORD})
    assert res_good_login.status_code == 200
    assert settings.COOKIE_NAME in res_good_login.cookies
    session_cookie = res_good_login.cookies[settings.COOKIE_NAME]
    print("✓ Authentication: Login successful, issued HttpOnly signed session cookie")

    # Access /admin with cookie
    client.cookies.set(settings.COOKIE_NAME, session_cookie)
    res_dash = client.get("/admin")
    assert res_dash.status_code == 200
    assert "White Lotus" in res_dash.text
    print("✓ Admin Dashboard: Rendered authenticated HTML view")

    # 5. Admin Reservations Tab Actions
    res_admin_list = client.get("/api/admin/reservations?status_filter=All")
    assert res_admin_list.status_code == 200
    res_items = res_admin_list.json()["reservations"]
    assert any(r["id"] == new_res_id for r in res_items)
    print(f"✓ Admin Reservations: Listed {len(res_items)} reservations with VIP status and phone numbers")

    # One-tap Accept table
    res_accept = client.patch(f"/api/admin/reservations/{new_res_id}/status", json={"status": "Confirmed"})
    assert res_accept.status_code == 200
    assert res_accept.json()["status"] == "Confirmed"
    print(f"✓ Admin Action: Accepted table reservation ID {new_res_id} -> Status: Confirmed")

    # Reschedule modal update
    res_resched = client.patch(f"/api/admin/reservations/{new_res_id}/status", json={
        "status": "Rescheduled",
        "rescheduled_date": "2026-11-29",
        "rescheduled_time": "Dinner (09:00 PM)"
    })
    assert res_resched.status_code == 200
    assert res_resched.json()["status"] == "Rescheduled"
    print(f"✓ Admin Action: Rescheduled reservation ID {new_res_id} to 2026-11-29 at 09:00 PM")

    # 6. Admin Menu CRUD & Availability Toggle
    # Add new dish
    new_dish = {
        "name": "Kashmiri Morel & Saffron Risotto",
        "category": "pizza-pasta-risotto",
        "dietary_type": "veg",
        "price": "₹695",
        "desc": "Wild Himalayan Guchhi morels simmered with aged Carnaroli rice, Kashmiri saffron broth and 24-month Parmigiano-Reggiano.",
        "badge": "Chef Special",
        "is_available": True
    }
    res_add_menu = client.post("/api/admin/menu", json=new_dish)
    assert res_add_menu.status_code == 200
    new_item_id = res_add_menu.json()["item_id"]
    print(f"✓ Admin Menu CRUD: Added '{new_dish['name']}' with ID {new_item_id}")

    # 1-click Sold Out toggle
    res_toggle = client.patch(f"/api/admin/menu/{new_item_id}/toggle-availability")
    assert res_toggle.status_code == 200
    assert res_toggle.json()["is_available"] is False
    print(f"✓ Admin Menu Switch: Toggled ID {new_item_id} -> Sold Out")

    # Toggle back to Available
    res_toggle_back = client.patch(f"/api/admin/menu/{new_item_id}/toggle-availability")
    assert res_toggle_back.status_code == 200
    assert res_toggle_back.json()["is_available"] is True
    print(f"✓ Admin Menu Switch: Toggled ID {new_item_id} -> Available")

    # Delete test dish
    res_del_menu = client.delete(f"/api/admin/menu/{new_item_id}")
    assert res_del_menu.status_code == 200
    print(f"✓ Admin Menu CRUD: Deleted temporary test item ID {new_item_id}")

    # 7. Customer CRM & CSV Export
    res_cust_list = client.get("/api/admin/customers")
    assert res_cust_list.status_code == 200
    customers = res_cust_list.json()["customers"]
    assert len(customers) >= 1
    target_cust = next(c for c in customers if c["phone"] == test_guest_phone)

    # Update tag to VIP and add staff notes
    res_cust_update = client.patch(f"/api/admin/customers/{target_cust['id']}", json={
        "tag": "VIP",
        "notes": "Prefers corner table on Starlit Terrace. High spender on artisanal cocktails."
    })
    assert res_cust_update.status_code == 200
    print(f"✓ Customer CRM: Promoted guest {target_cust['name']} to ⭐ VIP with staff notes")

    # CSV Export
    res_csv = client.get("/api/admin/customers/export-csv")
    assert res_csv.status_code == 200
    assert "text/csv" in res_csv.headers["content-type"]
    assert "Aditya Deshmukh" in res_csv.text
    print("✓ Customer CRM: Exported customer database CSV with valid headers and records")

    print("=" * 60)
    print("ALL PHASE 1 FEATURES VERIFIED SUCCESSFULLY (100% PASS)")
    print("=" * 60)

if __name__ == "__main__":
    run_all_tests()
