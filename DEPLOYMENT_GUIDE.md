# Campus Gabaa — Zero-Budget Public Cloud Deployment Guide

This guide provides reproducible, step-by-step instructions for deploying Campus Gabaa publicly to the internet with **$0.00 ongoing infrastructure cost**.

---

## 1. Hosting Architecture Overview

| Component | Free Platform / Provider | Free Tier Specification |
| :--- | :--- | :--- |
| **Web Application Server** | [Render.com](https://render.com) (or [Koyeb](https://koyeb.com)) | 750 free compute hours/month, automatic HTTPS/SSL, HTTP/2 |
| **Relational Database** | [Neon.tech](https://neon.tech) (Serverless Postgres) or Local Persistent SQLite | 0.5 GB persistent storage, pooling connection strings, free forever |
| **Static Assets Engine** | WhiteNoise 6.8 (Integrated) | Gzip/Brotli compression, cache-busting hashes, $0 CDN cost |
| **Health Monitoring** | [UptimeRobot](https://uptimerobot.com) | Free 5-minute ping on `/healthz/` to prevent cold-sleep |

---

## 2. Step-by-Step Deployment on Render.com

### Step 2.1: Push Repository to GitHub
1. Create a new repository on your GitHub account (e.g. `https://github.com/your-username/campus_gabaa`).
2. Add your GitHub remote and push:
   ```bash
   git remote add origin https://github.com/your-username/campus_gabaa.git
   git push -u origin main
   ```

### Step 2.2: Setup Free PostgreSQL on Neon.tech (Recommended)
1. Go to [neon.tech](https://neon.tech) and create a free account.
2. Create a project named `campus-gabaa`.
3. Copy the pooled connection string, which looks like:
   `postgresql://neondb_owner:password@ep-xyz.eu-central-1.aws.neon.tech/neondb?sslmode=require`

*(Alternative: You can deploy without PostgreSQL initially; the platform defaults to SQLite if `DATABASE_URL` is omitted).*

### Step 2.3: Create Web Service on Render
1. Log in to [Render.com](https://render.com) and click **New +** &rarr; **Web Service**.
2. Connect your GitHub repository: `campus_gabaa`.
3. Configure settings:
   - **Name:** `campus-gabaa`
   - **Region:** Frankfurt (EU Central) *(Closest free region for Ethiopian latency)*
   - **Branch:** `main`
   - **Root Directory:** *(Leave empty)*
   - **Runtime:** `Python 3`
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn config.wsgi:application --workers 2 --threads 2`
   - **Instance Type:** `Free`

### Step 2.4: Set Environment Variables on Render
Under the **Environment Variables** section, add:

| Key | Value | Notes |
| :--- | :--- | :--- |
| `DEBUG` | `False` | Disables debug mode for production security |
| `SECRET_KEY` | *(Click "Generate" or paste random 50-char string)* | Django cryptographic secret |
| `ALLOWED_HOSTS` | `.onrender.com,localhost,127.0.0.1` | Permits Render subdomain |
| `CSRF_TRUSTED_ORIGINS` | `https://*.onrender.com` | Prevents 403 CSRF rejection |
| `DATABASE_URL` | `postgresql://...neon.tech/neondb?sslmode=require` | *(Optional, if using Neon)* |
| `PRICE_STALE_DAYS` | `7` | Days before listings turn STALE |

### Step 2.5: Deploy and Verify
1. Click **Create Web Service**.
2. Render executes `./build.sh`, running:
   - `pip install -r requirements.txt`
   - `python manage.py collectstatic --no-input`
   - `python manage.py migrate`
   - Automatic seeding of initial Haramaya University demo products and shops.
3. Once the build completes, Render provides your live public URL:
   `https://campus-gabaa.onrender.com`

---

## 3. Post-Deployment Verification Checklist

Verify each of the following endpoints and actions from a mobile phone or incognito browser:

- [ ] **Liveness Check:** Visit `https://campus-gabaa.onrender.com/healthz/` &rarr; Returns `{"status": "healthy"}`.
- [ ] **Public Catalog:** Navigate to `/market/products/` &rarr; Verify 10 demo student items display with price comparisons.
- [ ] **Ranked Price Matrix:** Open `/market/products/100-sheet-ruled-exercise-book-a4/` &rarr; Verify multi-shop comparison table ranks cheapest vendor first and displays `#1 Best Deal` badge.
- [ ] **Language Negotiation:** Click language switcher in navbar &rarr; Switch to **Afaan Oromoo** and **አማርኛ** &rarr; Verify headings, buttons, and badges translate immediately.
- [ ] **Freshness Badges:** Confirm that items confirmed within 3 days display green `FRESH` and older items display yellow `EXPIRING` or red `STALE`.
- [ ] **Authentication:** Log in using demo credentials:
  - Moderator: `admin` / `CampusAdmin2026!`
  - Vendor: `aman_stationery` / `VendorPass2026!`
  - Student: `student_solomon` / `StudentPass2026!`
- [ ] **One-Click Refresh:** As vendor, open `/market/dashboard/` and click **Confirm Today** &rarr; Verify badge turns to `FRESH`.
- [ ] **Discrepancy Reporting:** As student, click **Report Issue** on any listing &rarr; Submit price discrepancy &rarr; Verify it appears in moderator queue at `/moderation/dashboard/`.

---

## 4. Preventing Cold-Start Sleeping (Free Tier Optimization)

Free instances sleep after 15 minutes of inactivity. To keep the service awake during academic presentations and evaluator reviews:

1. Create a free account at [UptimeRobot.com](https://uptimerobot.com).
2. Add a new HTTP(s) Monitor:
   - **URL:** `https://campus-gabaa.onrender.com/healthz/`
   - **Interval:** Every 10 minutes.
3. This sends a lightweight 10-byte ping that keeps the container warm and guarantees zero evaluator wait time.
