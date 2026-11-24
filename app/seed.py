import sys
from pathlib import Path
from datetime import datetime
from sqlalchemy.orm import Session
from app.config import settings
from app.database import engine, Base, SessionLocal
from app.models import AdminUser, MenuItem, Customer, Reservation
from app.security import hash_password

def seed_database(db: Session = None):
    # Ensure all tables exist
    Base.metadata.create_all(bind=engine)

    close_at_end = False
    if db is None:
        db = SessionLocal()
        close_at_end = True

    try:
        # 1. Seed Admin User
        admin_count = db.query(AdminUser).count()
        if admin_count == 0:
            admin = AdminUser(
                username=settings.ADMIN_USERNAME,
                password_hash=hash_password(settings.ADMIN_PASSWORD),
                full_name="White Lotus Floor Captain",
                role="owner"
            )
            db.add(admin)
            db.commit()
            print(f"[Seed] Created admin account: {settings.ADMIN_USERNAME}")

        # 2. Seed 166+ Menu Items from build_full_menu.py
        menu_count = db.query(MenuItem).count()
        if menu_count == 0:
            sys.path.append(str(Path(__file__).resolve().parent.parent))
            import build_full_menu
            items_to_add = []
            for idx, item in enumerate(build_full_menu.menu_data):
                m = MenuItem(
                    name=item.get("name", "Dish"),
                    category=item.get("category", "appetizers"),
                    dietary_type=item.get("type", "veg"),
                    price=item.get("price", "₹350"),
                    desc=item.get("desc", ""),
                    badge=item.get("badge", ""),
                    is_available=True,
                    sort_order=idx + 1
                )
                items_to_add.append(m)
            db.add_all(items_to_add)
            db.commit()
            print(f"[Seed] Successfully seeded {len(items_to_add)} menu items into SQLite.")

        # 3. Seed Sample Customer & Reservations for initial dashboard demonstration
        res_count = db.query(Reservation).count()
        if res_count == 0:
            sample_customer = Customer(
                phone="9823012345",
                name="Vikramaditya Shinde",
                email="vikram.shinde@example.com",
                total_bookings=3,
                last_visit_date="2026-11-20",
                preferred_zone="Imperial Velvet AC Lounge",
                tag="VIP",
                notes="Prefers corner booth with low ambient music; allergic to peanuts."
            )
            db.add(sample_customer)
            db.commit()
            db.refresh(sample_customer)

            sample_res1 = Reservation(
                booking_ref="WL-20261124-001",
                customer_id=sample_customer.id,
                guest_name=sample_customer.name,
                guest_phone=sample_customer.phone,
                guest_email=sample_customer.email,
                reservation_date="2026-11-25",
                time_slot="Dinner (8:00 PM)",
                party_size=4,
                dining_zone="Imperial Velvet AC Lounge",
                special_request="Anniversary celebration, needs quiet corner table.",
                status="Confirmed"
            )

            sample_customer2 = Customer(
                phone="9765432100",
                name="Pooja Kulkarni",
                email="pooja.k@example.com",
                total_bookings=1,
                last_visit_date="2026-11-24",
                preferred_zone="Starlit Garden Terrace",
                tag="Regular",
                notes="Loves open-air terrace seating."
            )
            db.add(sample_customer2)
            db.commit()
            db.refresh(sample_customer2)

            sample_res2 = Reservation(
                booking_ref="WL-20261124-002",
                customer_id=sample_customer2.id,
                guest_name=sample_customer2.name,
                guest_phone=sample_customer2.phone,
                guest_email=sample_customer2.email,
                reservation_date="2026-11-26",
                time_slot="Lunch (1:00 PM)",
                party_size=6,
                dining_zone="Starlit Garden Terrace",
                special_request="Family lunch with elders, need ground floor easy access.",
                status="Pending"
            )

            db.add_all([sample_res1, sample_res2])
            db.commit()
            print("[Seed] Seeded sample customers and reservations.")

    finally:
        if close_at_end:
            db.close()

if __name__ == "__main__":
    seed_database()
