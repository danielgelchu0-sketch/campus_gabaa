"""
WSGI compatibility entrypoint for cloud platforms (e.g., Render default start command).
Exposes the Django WSGI application callable as both `app` and `application`,
ensuring `gunicorn app:app` succeeds immediately without configuration mismatch.
"""
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

from config.wsgi import application

# Expose 'app' for Render's default 'gunicorn app:app' command
app = application
