# Campus Gabaa (GabaaHU)

> **Campus Shopping & Multi-Kiosk Price Comparison Platform**  
> Tailored for the **Haramaya University** Community (Main Campus, Agriculture Campus, Bate Market & Haramaya Town).

[![Django](https://img.shields.io/badge/Django-5.2-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Ready-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)
[![Zero Budget](https://img.shields.io/badge/Hosting%20Cost-%240.00%2Fmo-brightgreen?style=for-the-badge)](DEPLOYMENT_GUIDE.md)

---

## 1. Problem Statement & Motivation

Haramaya University (HU) students frequently face severe price fragmentation and information asymmetry when buying academic stationery, electronics, toiletries, snacks, and thesis print services. 

Across dorm kiosks (Blocks 1–60), campus gates, and Bate market, identical items (e.g., standard 100-page exercise books or flash drives) fluctuate widely in price. Due to lack of centralized pricing information, students waste significant time walking between distant kiosks or paying unnecessary markups. In addition, existing prices shift rapidly due to inflation, rendering word-of-mouth quotes obsolete.

**Campus Gabaa** solves this by providing:
1. **1-to-N Canonical Product Price Comparison:** Aggregates and ranks every participating campus kiosk and Bate merchant by price.
2. **Automated Price Freshness Badges:** Clear color-coded indicators (**FRESH** < 3 days, **EXPIRING** 3–7 days, **STALE** > 7 days).
3. **Crowd-Sourced Accuracy Verification:** Direct student reporting of price disparities and stockouts to campus moderators.
4. **Multilingual Interface:** Authentic localization in **Afaan Oromoo**, **Amharic (አማርኛ)**, and **English**.
5. **Zero-Budget Cloud Architecture:** Designed to run in production with $0.00 infrastructure overhead.

---

## 2. Core Capabilities

- **Responsive Catalog & Multi-Criteria Search:** Filter by category, campus zone (Main Campus Kiosks, Bate Gate, Bate Market, Haramaya Town), in-stock status, and price sorting.
- **Ranked Multi-Shop Matrix:** Cheaper shops are ranked first with potential savings highlighted (e.g., *"Save up to 30 ETB"*).
- **Merchant Management Portal:** One-click *"Confirm Price Today"* action refreshes verification timestamps without tedious re-typing.
- **Audit History:** Full log of price adjustments in `PriceHistory` for price transparency.
- **Community Moderation:** Student discrepancy reports queue for moderator resolution.
- **Mobile-First UX:** Ultra-lightweight SSR templates optimized for Ethiopian 3G/4G connections.

---

## 3. Technology Stack

- **Backend:** Python 3.14, Django 5.2 (Clean monolithic architecture)
- **Database:** PostgreSQL (Cloud production via `dj-database-url`) / SQLite (Local development)
- **Static Assets:** WhiteNoise 6.8 (Brotli/Gzip compression, cache-busting hashes)
- **Production Server:** Gunicorn 26.2 WSGI
- **Localization:** GNU gettext message catalogs (`.po` / `.mo`)
- **Frontend:** Semantic HTML5, Bootstrap 5.3, Bootstrap Icons, Vanilla JS

---

## 4. Local Installation & Quickstart

### Prerequisites
- Python 3.10+ (Tested on Python 3.14)
- Git

### Steps
1. **Clone the repository:**
   ```bash
   git clone https://github.com/danielgelchu0-sketch/campus_gabaa.git
   cd campus_gabaa
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   ```

5. **Apply database migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Seed realistic Haramaya University demonstration data:**
   ```bash
   python manage.py seed_campus_data
   ```

7. **Run the development server:**
   ```bash
   python manage.py runserver
   ```
   Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

---

## 5. Demonstration Accounts

| Role | Username | Password | Purpose |
| :--- | :--- | :--- | :--- |
| **Moderator / Admin** | `admin` | `CampusAdmin2026!` | Moderation queue & shop approvals |
| **Shop Owner** | `aman_stationery` | `VendorPass2026!` | Kiosk inventory & 1-click price refresh |
| **Student Buyer** | `student_solomon` | `StudentPass2026!` | Search, comparison & discrepancy reports |

---

## 6. Automated Testing

Run the full automated test suite (18 comprehensive tests):
```bash
python manage.py test
```

---

## 7. Zero-Budget Deployment

This project includes pre-configured deployment artifacts for **Render.com** and **Neon.tech**:
- `render.yaml`: Infrastructure-as-code specification.
- `Procfile`: Gunicorn production WSGI process.
- `build.sh`: Automated dependency installation, static collection, migrations, and conditional demo data seeding.

For detailed deployment steps, consult [`DEPLOYMENT_GUIDE.md`](DEPLOYMENT_GUIDE.md).

---

## 8. License & Academic Defense

Developed as a Senior Graduation Capstone Project for the Department of Computing / Software Engineering at **Haramaya University**, Ethiopia. Released under the MIT License.
