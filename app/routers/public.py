import urllib.parse
from datetime import datetime
import random
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from sqlalchemy import or_

from pydantic import BaseModel, Field
from app.database import get_db
from app.config import settings
from app.models import MenuItem, Customer, Reservation, BanquetEnquiry, AnalyticsEvent
from app.schemas import ReservationCreate, BanquetEnquiryCreate
from app.security import check_rate_limit, get_client_ip, log_security_event

class DataDeletionRequest(BaseModel):
    phone: str = Field(..., min_length=10, max_length=20)
    reason: Optional[str] = Field("User privacy erasure request", max_length=255)

router = APIRouter(prefix="/api", tags=["Public"])

@router.get("/menu")
def get_public_menu(
    dietary: Optional[str] = "all", # all, veg, nonveg, bar
    category: Optional[str] = None,
    q: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(MenuItem)

    if dietary and dietary != "all":
        query = query.filter(MenuItem.dietary_type == dietary)

    if category and category != "all":
        query = query.filter(MenuItem.category == category)

    if q and q.strip():
        term = f"%{q.strip()}%"
        query = query.filter(or_(
            MenuItem.name.ilike(term),
            MenuItem.desc.ilike(term),
            MenuItem.badge.ilike(term)
        ))

    items = query.order_by(MenuItem.sort_order.asc(), MenuItem.id.asc()).all()

    # Category summaries
    categories = [
        {"id": "all", "label": "Full Culinary Deck"},
        {"id": "appetizers", "label": "Small Plates & Appetizers"},
        {"id": "soups-salads-bao", "label": "Soups, Salads & Bao"},
        {"id": "pizza-pasta-risotto", "label": "Pizza, Pasta & Risotto"},
        {"id": "bowls-continental", "label": "Global Bowls & Steaks"},
        {"id": "breads-rice-noodles", "label": "Breads, Rice & Noodles"},
        {"id": "mains", "label": "Imperial Mains & Curries"},
        {"id": "desserts-icecream", "label": "Desserts & Natural Ice Creams"},
        {"id": "bar-mixology", "label": "The Lotus Bar & Cellar"}
    ]

    return {
        "count": len(items),
        "categories": categories,
        "items": [
            {
                "id": it.id,
                "name": it.name,
                "category": it.category,
                "dietary_type": it.dietary_type,
                "price": it.price,
                "desc": it.desc,
                "badge": it.badge,
                "is_available": it.is_available
            }
            for it in items
        ]
    }

@router.post("/reservations")
def create_reservation(
    payload: ReservationCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    # Rate limit: 10 per minute per IP
    client_ip = request.client.host if request.client else "127.0.0.1"
    if not check_rate_limit(f"res_submit_{client_ip}", max_calls=10, period_seconds=60):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many reservation requests. Please wait a moment before trying again."
        )

    # Clean phone number
    phone = payload.guest_phone

    # 1. Create or update Customer CRM record
    customer = db.query(Customer).filter(Customer.phone == phone).first()
    if customer:
        customer.total_bookings += 1
        customer.last_visit_date = payload.reservation_date
        customer.preferred_zone = payload.dining_zone
        if payload.guest_email and not customer.email:
            customer.email = payload.guest_email
        customer.name = payload.guest_name # update if changed
    else:
        customer = Customer(
            phone=phone,
            name=payload.guest_name,
            email=payload.guest_email or "",
            total_bookings=1,
            last_visit_date=payload.reservation_date,
            preferred_zone=payload.dining_zone,
            tag="Regular",
            notes=f"First booked on {datetime.utcnow().strftime('%Y-%m-%d')} for {payload.dining_zone}"
        )
        db.add(customer)
        db.flush()

    # 2. Generate unique booking ref
    date_code = datetime.utcnow().strftime("%Y%m%d")
    rand_code = random.randint(1000, 9999)
    booking_ref = f"WL-{date_code}-{rand_code}"

    # 3. Create Reservation
    reservation = Reservation(
        booking_ref=booking_ref,
        customer_id=customer.id,
        guest_name=payload.guest_name,
        guest_phone=phone,
        guest_email=payload.guest_email or "",
        reservation_date=payload.reservation_date,
        time_slot=payload.time_slot,
        party_size=payload.party_size,
        dining_zone=payload.dining_zone,
        special_request=payload.special_request or "",
        status="Pending"
    )
    db.add(reservation)

    # 4. Log analytics event
    event = AnalyticsEvent(
        event_type="reservation_submitted",
        details=f"{payload.dining_zone} ({payload.party_size} guests)",
        ip_hash=client_ip,
        date_str=datetime.utcnow().strftime("%Y-%m-%d")
    )
    db.add(event)

    db.commit()
    db.refresh(reservation)

    # 5. Build pre-filled WhatsApp alert link to Floor Captain
    special_note = f"\n*Special Request:* {payload.special_request}" if payload.special_request else ""
    msg = (
        f"🌸 *WHITE LOTUS PUNE — NEW VIP TABLE RESERVATION*\n\n"
        f"• *Booking Ref:* `{booking_ref}`\n"
        f"• *Guest:* {payload.guest_name}\n"
        f"• *Phone:* {phone}\n"
        f"• *Date:* {payload.reservation_date}\n"
        f"• *Slot:* {payload.time_slot}\n"
        f"• *Party Size:* {payload.party_size} Diners\n"
        f"• *Preferred Zone:* {payload.dining_zone}{special_note}\n\n"
        f"_Please confirm table allocation from Admin Dashboard._"
    )
    whatsapp_url = f"https://wa.me/{settings.CAPTAIN_WHATSAPP}?text={urllib.parse.quote(msg)}"

    return {
        "success": True,
        "booking_ref": booking_ref,
        "reservation_id": reservation.id,
        "guest_name": payload.guest_name,
        "status": "Pending",
        "whatsapp_url": whatsapp_url,
        "message": "Your reservation has been received and sent to Floor Captain for priority confirmation."
    }

@router.post("/banquets")
def create_banquet_enquiry(
    payload: BanquetEnquiryCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    client_ip = request.client.host if request.client else "127.0.0.1"
    if not check_rate_limit(f"banquet_submit_{client_ip}", max_calls=10, period_seconds=60):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests. Please wait a moment."
        )

    # 1. Auto-sync or create Customer CRM profile
    phone = payload.contact_phone
    customer = db.query(Customer).filter(Customer.phone == phone).first()
    if customer:
        customer.total_bookings += 1
        customer.tag = "Corporate" if "Corporate" in payload.event_type else customer.tag
        if payload.contact_email and not customer.email:
            customer.email = payload.contact_email
        customer.notes = f"{customer.notes}\n[Banquet] {payload.event_type} for {payload.estimated_guests} guests on {payload.event_date}".strip()
    else:
        customer = Customer(
            phone=phone,
            name=payload.contact_name,
            email=payload.contact_email or "",
            total_bookings=1,
            last_visit_date=payload.event_date,
            preferred_zone="Private Banquet Suite",
            tag="Corporate" if "Corporate" in payload.event_type else "Regular",
            notes=f"[Banquet Lead] {payload.event_type} for {payload.estimated_guests} guests on {payload.event_date}"
        )
        db.add(customer)

    # 2. Generate unique banquet enquiry reference
    date_code = datetime.utcnow().strftime("%Y%m%d")
    rand_code = random.randint(100, 999)
    enquiry_ref = f"WLB-{date_code}-{rand_code}"

    # 3. Create Banquet Enquiry record
    enquiry = BanquetEnquiry(
        enquiry_ref=enquiry_ref,
        contact_name=payload.contact_name,
        contact_phone=phone,
        contact_email=payload.contact_email or "",
        event_type=payload.event_type,
        event_date=payload.event_date,
        estimated_guests=payload.estimated_guests,
        cuisine_preference=payload.cuisine_preference,
        special_requests=payload.special_requests or "",
        status="New"
    )
    db.add(enquiry)

    # 4. Analytics event
    event = AnalyticsEvent(
        event_type="banquet_submitted",
        details=f"{payload.event_type} ({payload.estimated_guests} pax)",
        ip_hash=client_ip,
        date_str=datetime.utcnow().strftime("%Y-%m-%d")
    )
    db.add(event)

    db.commit()
    db.refresh(enquiry)

    # 5. WhatsApp alert for Banquet Event coordinator
    banquet_msg = (
        f"🥂 *WHITE LOTUS PUNE — NEW PRIVATE BANQUET ENQUIRY*\n\n"
        f"• *Ref:* `{enquiry_ref}`\n"
        f"• *Host:* {payload.contact_name}\n"
        f"• *Phone:* {phone}\n"
        f"• *Event Type:* {payload.event_type}\n"
        f"• *Date:* {payload.event_date}\n"
        f"• *Guests:* {payload.estimated_guests} People\n"
        f"• *Cuisine / Bar:* {payload.cuisine_preference}\n"
        f"• *Notes:* {payload.special_requests or 'None'}\n\n"
        f"_Please reach out to guest with bespoke banquet proposal._"
    )
    whatsapp_url = f"https://wa.me/{settings.CAPTAIN_WHATSAPP}?text={urllib.parse.quote(banquet_msg)}"

    return {
        "success": True,
        "enquiry_ref": enquiry_ref,
        "enquiry_id": enquiry.id,
        "whatsapp_url": whatsapp_url,
        "message": "Your banquet enquiry has been registered. Our events coordinator will contact you shortly."
    }

@router.post("/analytics/track")
def track_analytics(request: Request, db: Session = Depends(get_db)):
    """Lightweight first-party page view / interaction event tracking"""
    client_ip = get_client_ip(request)
    event = AnalyticsEvent(
        event_type="page_view",
        details="home_view",
        ip_hash=client_ip,
        date_str=datetime.utcnow().strftime("%Y-%m-%d")
    )
    db.add(event)
    db.commit()
    return {"status": "ok"}

# --- PRIVACY & DPDP DATA ERASURE (Legal & Compliance 12.3) ---
@router.post("/privacy/data-deletion")
def request_data_deletion(
    payload: DataDeletionRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """Allows guests to request permanent deletion or anonymization of their stored phone/name under DPDP Act 2023"""
    client_ip = get_client_ip(request)
    clean_p = payload.phone.replace("+", "").strip()

    customer = db.query(Customer).filter(Customer.phone.ilike(f"%{clean_p}%")).first()
    if customer:
        cust_name = customer.name
        # Delete associated reservations or anonymize
        db.query(Reservation).filter(Reservation.customer_id == customer.id).delete()
        db.delete(customer)
        db.commit()
        log_security_event("DATA_DELETION", f"Deleted CRM record for customer {cust_name} (phone {clean_p})", client_ip)
        return {
            "success": True,
            "message": "Your personal profile and table reservation history have been permanently purged from our database in compliance with the DPDP Act 2023."
        }
    else:
        log_security_event("DATA_DELETION_NOT_FOUND", f"No record found for phone {clean_p}", client_ip)
        return {
            "success": True,
            "message": "No customer record was associated with this phone number. Your data is not stored."
        }
