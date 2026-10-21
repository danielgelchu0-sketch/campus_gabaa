#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "==> Upgrading pip..."
pip install --upgrade pip

echo "==> Installing dependencies..."
pip install -r requirements.txt

echo "==> Collecting static assets via WhiteNoise..."
python manage.py collectstatic --no-input

echo "==> Applying database migrations..."
python manage.py migrate

echo "==> Checking if initial seed data is present..."
python manage.py shell -c "
from market.models import Product
from django.core.management import call_command
if not Product.objects.exists():
    print('==> Seeding initial Haramaya University demonstration data...')
    call_command('seed_campus_data')
else:
    print('==> Catalog data already present, skipping seed.')
"

echo "==> Build completed successfully!"
