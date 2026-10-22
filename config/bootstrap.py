"""
Automatic cloud deployment bootstrapper for Campus Gabaa.
Safeguards against production 500 errors when build commands are misconfigured
in platform dashboards (such as Render or Koyeb).
"""
import os
import sys
from pathlib import Path

_bootstrapped = False

def ensure_production_ready():
    """
    Ensures that staticfiles directory exists, database migrations are applied,
    and seed data is loaded when running on cloud hosts.
    """
    global _bootstrapped
    if _bootstrapped:
        return
    _bootstrapped = True

    try:
        from django.conf import settings
        from django.core.management import call_command

        # 1. Ensure staticfiles directory exists and assets are collected
        static_root = Path(settings.STATIC_ROOT)
        static_root.mkdir(parents=True, exist_ok=True)
        if not any(static_root.iterdir()):
            sys.stdout.write("==> Cloud Bootstrapper: Collecting static assets...\n")
            sys.stdout.flush()
            call_command('collectstatic', interactive=False, verbosity=0)

        # 2. Fast check: Only run migrations if tables don't exist yet
        from django.db import connection
        existing_tables = connection.introspection.table_names()
        if 'market_product' not in existing_tables:
            sys.stdout.write("==> Cloud Bootstrapper: Applying initial database migrations...\n")
            sys.stdout.flush()
            call_command('migrate', interactive=False, verbosity=0)

        # 3. Seed demonstration data if product catalog is empty
        from market.models import Product
        if not Product.objects.exists():
            sys.stdout.write("==> Cloud Bootstrapper: Seeding initial Haramaya University demonstration data...\n")
            sys.stdout.flush()
            call_command('seed_campus_data')
            sys.stdout.write("==> Cloud Bootstrapper: Demonstration data seeded successfully.\n")
            sys.stdout.flush()

        # 4. Explicitly guarantee default admin and vendor accounts with active credentials
        try:
            from accounts.models import User
            admin_user, _ = User.objects.get_or_create(
                username='admin',
                defaults={
                    'email': 'admin@campusgabaa.hu.edu.et',
                    'first_name': 'Dr. Dawit',
                    'last_name': 'Tadesse',
                    'role': User.ROLE_MODERATOR,
                    'is_staff': True,
                    'is_superuser': True,
                }
            )
            admin_user.set_password('CampusAdmin2026!')
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.role = User.ROLE_MODERATOR
            admin_user.save()

            vendor_user, _ = User.objects.get_or_create(
                username='aman_stationery',
                defaults={
                    'email': 'aman@kiosk.hu.edu.et',
                    'first_name': 'Aman',
                    'last_name': 'Kedir',
                    'role': User.ROLE_SHOP_OWNER,
                    'is_verified_vendor': True,
                }
            )
            vendor_user.set_password('VendorPass2026!')
            vendor_user.role = User.ROLE_SHOP_OWNER
            vendor_user.is_verified_vendor = True
            vendor_user.save()
            sys.stdout.write("==> Cloud Bootstrapper: Verified admin and vendor login credentials.\n")
            sys.stdout.flush()
        except Exception as _user_err:
            sys.stderr.write(f"==> Cloud Bootstrapper User Sync Note: {_user_err}\n")
            sys.stderr.flush()

    except Exception as exc:
        sys.stderr.write(f"==> Cloud Bootstrapper Note: {exc}\n")
        sys.stderr.flush()
