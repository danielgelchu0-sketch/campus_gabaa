# Campus Gabaa — Project Status & Implementation Log

*Last Updated: 2026-10-21*

## 1. Project Overview
- **Project Name:** Campus Gabaa (GabaaHU)
- **Problem Statement:** Haramaya University students and staff face price disparities, high search friction, and out-of-date product information when purchasing essentials (stationery, electronics, personal care, textbooks, snacks) across campus kiosks, Bate market, and Haramaya town. Campus Gabaa provides a multilingual, mobile-friendly discovery and price-comparison platform with transparency on price freshness and community accuracy reporting.
- **Target Audience:** Haramaya University students/faculty, local retail shops & merchants in Bate & Haramaya.
- **Languages:** English, Afaan Oromo, Amharic.
- **Tech Stack:** Python 3.14, Django 5.2, PostgreSQL/SQLite, WhiteNoise, Gunicorn, HTML5/CSS3/Vanilla JS.

---

## 2. Milestone Progress Tracker
*Status Legend: [COMPLETE], [IN PROGRESS], [PENDING], [BLOCKED]*

| Component | Status | Details |
| :--- | :--- | :--- |
| **Environment & Git Setup** | COMPLETE | Python 3.14 venv, clean dependencies, git initialized, .gitignore, .env |
| **Django Project Structure** | IN PROGRESS | Creating core apps: `accounts`, `core`, `market`, `moderation` |
| **Relational Data Models** | PENDING | User/Role, Shop, Category, Product, Listing, PriceHistory, Report |
| **Authentication & Roles** | PENDING | Student/General user, Shop Owner, Admin/Moderator |
| **Product Discovery & Comparison** | PENDING | Full search, category filter, multi-shop price matrix, freshness badge |
| **Shop Management Portal** | PENDING | Owner onboarding, listing creation, price update & stock toggle |
| **Moderation & Reporting** | PENDING | Stale/inaccurate price reporting, admin review dashboard |
| **Multilingual Localization** | PENDING | English, Afaan Oromo, Amharic translations (.po/.mo) |
| **Automated Tests** | PENDING | Model, view, permission, and workflow test suites |
| **Seed Demo Data** | PENDING | Realistic Haramaya/Bate campus shops and common student items |
| **Zero-Budget Deployment** | PENDING | Render / Koyeb build configurations, Procfile, runtime settings |
| **Documentation & Guides** | PENDING | Architecture ERD, Presentation Q&A Defense Guide, Walkthrough script |

---

## 3. Important Architectural Decisions
1. **Monolithic Architecture**: Single Django application with clean modular apps (`accounts`, `core`, `market`, `moderation`) to avoid microservice latency, operational complexity, and network failure modes on free hosting tiers.
2. **Product Identity vs. Shop Listing Separation**: Products exist as canonical catalog entities (`Product`), and shops attach their respective pricing, availability, and updates via `Listing` relations. This allows true 1-to-N price comparison without data duplication.
3. **Price Freshness Logic**: Every listing tracks `updated_at` and `last_price_confirmed_at`. A configurable threshold (`PRICE_STALE_DAYS`, default 7) dynamically tags listings as "Fresh", "Expiring Soon", or "Stale" to prevent students from traveling on stale information.
4. **Server-Side Rendered Templates with Progressive Enhancement**: Mobile-first responsive CSS without heavy frontend frameworks to maintain fast 3G/4G loading speeds around Haramaya.

---

## 4. Current Blockers & Next Actions
- **Blockers:** None.
- **Immediate Next Step:** Generate Django project (`campus_gabaa_project`), establish modular apps, configure settings for localization, database fallback, and WhiteNoise.
