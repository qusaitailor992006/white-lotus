import html
import re
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator

def clean_text(v: Optional[str]) -> str:
    if not v:
        return ""
    # Strip and escape HTML to prevent XSS
    return html.escape(v.strip())

def clean_phone(v: str) -> str:
    cleaned = re.sub(r"[^\d+]", "", v)
    if len(cleaned) < 10:
        raise ValueError("Please provide a valid phone number with at least 10 digits.")
    return cleaned

class LoginRequest(BaseModel):
    username: str
    password: str

    @field_validator("username")
    def sanitize_username(cls, v):
        return clean_text(v)

class ReservationCreate(BaseModel):
    guest_name: str = Field(..., min_length=2, max_length=100)
    guest_phone: str = Field(..., min_length=10, max_length=20)
    guest_email: Optional[str] = Field("", max_length=100)
    reservation_date: str = Field(..., min_length=8, max_length=30)
    time_slot: str = Field(..., min_length=3, max_length=50)
    party_size: int = Field(2, ge=1, le=50)
    dining_zone: str = Field("Starlit Garden Terrace", max_length=100)
    special_request: Optional[str] = Field("", max_length=500)

    @field_validator("guest_name", "special_request", "dining_zone", "time_slot", "reservation_date")
    def sanitize_strings(cls, v):
        return clean_text(v)

    @field_validator("guest_phone")
    def validate_phone(cls, v):
        return clean_phone(v)

class ReservationUpdateStatus(BaseModel):
    status: str = Field(..., pattern="^(Pending|Confirmed|Rescheduled|Rejected)$")
    rejection_reason: Optional[str] = ""
    rescheduled_date: Optional[str] = ""
    rescheduled_time: Optional[str] = ""

    @field_validator("rejection_reason", "rescheduled_date", "rescheduled_time")
    def sanitize_fields(cls, v):
        return clean_text(v)

class MenuItemCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    category: str = Field(..., min_length=2, max_length=50)
    dietary_type: str = Field(..., pattern="^(veg|nonveg|bar)$")
    price: str = Field(..., min_length=1, max_length=50)
    desc: Optional[str] = Field("", max_length=500)
    badge: Optional[str] = Field("", max_length=50)
    is_available: bool = True

    @field_validator("name", "category", "price", "desc", "badge")
    def sanitize_strings(cls, v):
        return clean_text(v)

class MenuItemUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    dietary_type: Optional[str] = None
    price: Optional[str] = None
    desc: Optional[str] = None
    badge: Optional[str] = None
    is_available: Optional[bool] = None

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    preferred_zone: Optional[str] = None
    tag: Optional[str] = None
    notes: Optional[str] = None

    @field_validator("name", "email", "preferred_zone", "tag", "notes")
    def sanitize_strings(cls, v):
        return clean_text(v)

class BanquetEnquiryCreate(BaseModel):
    contact_name: str = Field(..., min_length=2, max_length=100)
    contact_phone: str = Field(..., min_length=10, max_length=20)
    contact_email: Optional[str] = Field("", max_length=100)
    event_type: str = Field(..., min_length=2, max_length=50)
    event_date: str = Field(..., min_length=8, max_length=30)
    estimated_guests: int = Field(30, ge=10, le=500)
    cuisine_preference: str = Field("Veg + Non-Veg", max_length=50)
    special_requests: Optional[str] = Field("", max_length=500)

    @field_validator("contact_name", "event_type", "event_date", "cuisine_preference", "special_requests")
    def sanitize_strings(cls, v):
        return clean_text(v)

    @field_validator("contact_phone")
    def validate_phone(cls, v):
        return clean_phone(v)

class BanquetStatusUpdate(BaseModel):
    status: str = Field(..., pattern="^(New|Quoted|Confirmed|Closed)$")
    notes: Optional[str] = ""

    @field_validator("notes")
    def sanitize_notes(cls, v):
        return clean_text(v)
