"""
Gunicorn configuration file for Campus Gabaa.
Automatically detected by Gunicorn to configure port binding, workers, and logging.
Fixes Render's 'Port scan timeout reached, no open ports detected' error by
explicitly binding to 0.0.0.0:$PORT.
"""
import os

# Render injects the PORT environment variable (typically 10000)
port = os.environ.get("PORT", "10000")
bind = f"0.0.0.0:{port}"

# Concurrency tuning for free tier container memory limits
workers = int(os.environ.get("WEB_CONCURRENCY", "1"))
threads = 4
timeout = 120
keepalive = 5

# Stream logs directly to stdout/stderr for Render log capture
accesslog = "-"
errorlog = "-"
loglevel = "info"
