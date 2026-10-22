"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()

# Cloud deployment safeguard: automatically apply migrations and collect static if omitted
try:
    from config.bootstrap import ensure_production_ready
    ensure_production_ready()
except Exception as _bootstrap_err:
    import sys
    sys.stderr.write(f"WSGI Bootstrap warning: {_bootstrap_err}\n")
