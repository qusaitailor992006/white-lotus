from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class AdminUser(Base):
    __tablename__ = "admin_users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), default="Floor Captain")
    role = Column(String(50), default="manager")
    created_at = Column(DateTime, default=datetime.utcnow)

class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), index=True, nullable=False)
    category = Column(String(50), index=True, nullable=False)
    dietary_type = Column(String(20), index=True, nullable=False) # veg, nonveg, bar
    price = Column(String(50), nullable=False)
    desc = Column(Text, default="")
    badge = Column(String(50), default="")
    is_available = Column(Boolean, default=True, index=True)
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String(20), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    email = Column(String(100), default="")
    total_bookings = Column(Integer, default=1)
    last_visit_date = Column(String(30), default="")
    preferred_zone = Column(String(100), default="Starlit Garden Terrace")
    tag = Column(String(50), default="Regular") # Regular, VIP, Corporate
    notes = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    reservations = relationship("Reservation", back_populates="customer")

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    booking_ref = Column(String(50), unique=True, index=True, nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    guest_name = Column(String(100), nullable=False)
    guest_phone = Column(String(20), index=True, nullable=False)
    guest_email = Column(String(100), default="")
    reservation_date = Column(String(30), index=True, nullable=False)
    time_slot = Column(String(50), nullable=False)
    party_size = Column(Integer, default=2)
    dining_zone = Column(String(100), default="Starlit Garden Terrace")
    special_request = Column(Text, default="")
    status = Column(String(30), default="Pending", index=True) # Pending, Confirmed, Rescheduled, Rejected
    rejection_reason = Column(String(255), default="")
    rescheduled_date = Column(String(30), default="")
    rescheduled_time = Column(String(50), default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    customer = relationship("Customer", back_populates="reservations")

class BanquetEnquiry(Base):
    __tablename__ = "banquet_enquiries"

    id = Column(Integer, primary_key=True, index=True)
    enquiry_ref = Column(String(50), unique=True, index=True, nullable=False)
    contact_name = Column(String(100), nullable=False)
    contact_phone = Column(String(20), index=True, nullable=False)
    contact_email = Column(String(100), default="")
    event_type = Column(String(50), nullable=False) # Birthday, Anniversary, Corporate, Family Gathering, Cocktail Soiree
    event_date = Column(String(30), nullable=False)
    estimated_guests = Column(Integer, default=30)
    cuisine_preference = Column(String(50), default="Veg + Non-Veg") # Pure Veg, Veg + Non-Veg, Bar Package
    special_requests = Column(Text, default="")
    status = Column(String(30), default="New", index=True) # New, Quoted, Confirmed, Closed
    notes = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)

class AnalyticsEvent(Base):
    __tablename__ = "analytics_events"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String(50), index=True, nullable=False) # page_view, menu_view, reservation_submitted, banquet_submitted
    details = Column(String(255), default="")
    ip_hash = Column(String(64), default="")
    date_str = Column(String(10), index=True, nullable=False) # YYYY-MM-DD
    created_at = Column(DateTime, default=datetime.utcnow)
