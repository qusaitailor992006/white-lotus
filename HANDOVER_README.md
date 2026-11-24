# White Lotus: Food Vibe Folks — Operational Web Platform & Management System

> **Luxury Fine Dining Web Application, Booking Engine & Operations Dashboard**  
> **Destination:** 202, 203 Saras Baug Road, Opposite Sanas Ground, Parvati, Pune 411009  
> **Floor Desk WhatsApp:** +91 95135 75757  
> **Google Rating:** 4.6 ★ (1,660+ Verified Diners)

---

## 1. Executive System Architecture

The White Lotus web platform is built as a complete, modern Python full-stack application that marries the **bespoke luxury visual identity** (pearl alabaster `#FAF8F5`, deep lotus emerald `#13382C`, and champagne gold `#C59B47` with interactive 60 FPS floating 3D lotus petals) with a **high-performance operational backend**:

```
                               ┌────────────────────────────────────────────────────────┐
                               │                    PUBLIC DINERS                       │
                               │  • 60 FPS 3D Petals  • 166+ Menu with Dietary Filter    │
                               │  • VIP Table Booking • Banquets (20-150 Pax) • Maps    │
                               └──────────────────────────┬─────────────────────────────┘
                                                          │ HTTP / JSON API
                                                          ▼
┌───────────────────────────────────────────────────────────────────────────────────────┐
│                                   FASTAPI APPLICATION                                 │
│  ├── /                      Public Luxury Dining Portal                               │
│  ├── /api/menu              Live Menu Catalog & Instant Search                        │
│  ├── /api/reservations      Commission-Free Booking + Auto CRM Sync                   │
│  ├── /api/banquets          Private Events & Celebration Inquiries                    │
│  ├── /admin/login           Bcrypt Password Authentication Gate                       │
│  ├── /admin                 Protected Executive Management Dashboard                 │
│  └── /api/admin/*           CRUD Operations (Reservations, Menu, CRM, Banquets)       │
└──────────────────────────┬──────────────────────────────┬─────────────────────────────┘
                           │ SQLAlchemy ORM               │ Pre-filled Alerts
                           ▼                              ▼
                 ┌───────────────────┐         ┌────────────────────────┐
                 │  SQLite Database  │         │   FLOOR CAPTAIN DESK   │
                 │  (white_lotus.db) │         │    +91 95135 75757     │
                 │   + /backups/     │         │   Instant WhatsApp     │
                 └───────────────────┘         └────────────────────────┘
```

---

## 2. Core Operational Capabilities

### Phase 1: Core Operational Engine
1. **Private Admin Dashboard (`/admin` & `/admin/login`):**
   - Secure staff and management authentication powered by `bcrypt` password hashing.
   - Session management via `HttpOnly; SameSite=Strict; Path=/` signed JWT cookies.
   - All `/admin` pages and `/api/admin/*` endpoints strictly blocked to unauthenticated visitors (auto-redirect to `/admin/login`).
   - 100% mobile-responsive layout designed for handheld smartphone operation by on-duty floor captains.

2. **Table Reservation Management:**
   - Public booking modal capturing Guest Name, Mobile Number, Date, Time Slot, Party Size, Dining Sanctuary (*Starlit Garden Terrace* / *Imperial Velvet AC Lounge*), and Special Requests.
   - Admin view with filters (`All`, `Pending`, `Confirmed`, `Rescheduled`, `Rejected`) and real-time live search.
   - One-tap staff status updates: **Accept Table**, **Reject Table**, and **Reschedule** (modal with date & time pickers).

3. **Live Menu Management (166+ Items):**
   - Auto-seeded SQLite database on initial run with all 166 official items across 8 categories (Appetizers, Soups/Salads/Bao, Pizza/Pasta/Risotto, Bowls & Steaks, Breads/Rice/Noodles, Imperial Mains, Desserts & Ice Creams, The Lotus Bar).
   - Public site dynamically synchronizes with `/api/menu`.
   - Admin 1-click **Available / Sold Out** switch that automatically dims sold-out dishes on the public menu with a visible status tag.
   - Add new dish, edit pricing/description/badge, and delete capabilities.

4. **Customer CRM System:**
   - Automatically builds or updates guest profiles keyed by phone number on every booking or banquet inquiry.
   - Tracks: Full Name, Phone, Email, Total Visits, Last Visit Date, Preferred Sanctuary, VIP/Regular tag, and private Staff Notes (e.g. food allergies, preferred tables).
   - One-click **Export CSV** button for marketing and guest loyalty lists.

5. **WhatsApp Automation:**
   - On public booking, generates an instant WhatsApp reservation alert pre-addressed to the Floor Captain at **+91 95135 75757**.
   - Admin dashboard includes one-click **Send WhatsApp Confirmation** and **Send Reschedule Update** buttons to message guests in 3 seconds.

---

### Phase 2: Growth, Banquets & SEO Layer
6. **Banquet & Private Event Booking System:**
   - Public dedicated inquiry modal for celebrations of **20 to 150 guests** (Birthdays, Anniversaries, Corporate Dinners, Family Gatherings, Cocktail Soirées).
   - Auto-syncs corporate and celebration hosts directly into the Customer CRM.
   - Admin Banquets Tab to track leads (`New`, `Quoted`, `Confirmed`, `Closed`) with one-tap WhatsApp proposal messaging.

7. **Analytics Dashboard:**
   - Lightweight, privacy-safe first-party traffic and demand tracking stored in SQLite (zero external tracking scripts or tracking cookies).
   - Admin overview KPI summary cards: Total Page Views, Direct Reservations, Confirmation Ratio, Banquet Leads, and 7-day engagement trend bars.

8. **Google Integration, Local SEO & Automated Backups:**
   - Interactive Google Maps embed for **White Lotus: Food Vibe Folks, Saras Baug Rd, Pune**.
   - Quick-action **Get Live Directions** and **Leave a Google Review** CTA buttons.
   - Complete `Restaurant` JSON-LD schema, OpenGraph tags, `/robots.txt`, and canonical `/sitemap.xml`.
   - Standalone `backup_db.py` script that creates timestamped SQLite backups in `/backups` and performs automatic integrity verification (`PRAGMA integrity_check`).

---

## 3. Quick Start & Local Run

### Prerequisites
- Python 3.10+ installed

### Setup & Run in 3 Commands

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment (already pre-configured in `.env`):**
   ```bash
   # Ensure .env exists (sample provided in .env.example)
   ```

3. **Start the application:**
   ```bash
   python run.py
   ```

4. **Open in your browser:**
   - **Public Luxury Portal:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
   - **Admin Staff Login:** [http://127.0.0.1:8000/admin/login](http://127.0.0.1:8000/admin/login)
   - **Admin Command Dashboard:** [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

---

## 4. Default Admin Credentials

| Parameter | Default Value | Notes |
|---|---|---|
| **Admin Username** | `lotus_admin` | Change in `.env` |
| **Admin Password** | `Lotus@Pune2026!` | Hashed via `bcrypt` |
| **Floor Captain WhatsApp** | `919513575757` | Configurable in `.env` |
| **Session Lifetime** | 7 Days | `HttpOnly; SameSite=Strict` cookie |

---

## 5. Automated Database Backups

Run the standalone backup script at any time or schedule via cron:

```bash
python backup_db.py
```

- Creates a verified snapshot in `/backups/white_lotus_backup_YYYYMMDD_HHMMSS.db`.
- Automatically tests SQLite integrity (`PRAGMA integrity_check`).
- Automatically rotates and retains the latest 10 backup archives.

---

## 6. Complete Verification Test Suites

To verify all system features, run the automated test suites:

```bash
# Verify Phase 1: Auth, Reservations, Menu CRUD, CRM, WhatsApp
python test_phase1.py

# Verify Phase 2: Banquets, Analytics, Maps, SEO, Backups
python test_phase2.py
```

Both test suites achieve **100% PASS** on clean installs.
