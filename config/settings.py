"""
Django settings for Campus Gabaa (GabaaHU) project.
A campus shopping & price-comparison platform for Haramaya University community.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file if present
load_dotenv(BASE_DIR / '.env')

# Security Settings
SECRET_KEY = os.getenv(
    'SECRET_KEY',
    'django-insecure-campus-gabaa-capstone-dev-key-change-in-prod-xyz123'
)

DEBUG = os.getenv('DEBUG', 'True').lower() in ('true', '1', 'yes')

# Allowed Hosts: Ensure .onrender.com, localhost, and 127.0.0.1 are always included
_env_hosts = os.getenv('ALLOWED_HOSTS', '')
ALLOWED_HOSTS = [
    '.onrender.com',
    'localhost',
    '127.0.0.1',
]
if _env_hosts:
    for host in _env_hosts.split(','):
        h = host.strip()
        if h and h not in ALLOWED_HOSTS:
            ALLOWED_HOSTS.append(h)

if '*' in ALLOWED_HOSTS:
    ALLOWED_HOSTS = ['*']

# CSRF trusted origins for modern Django versions (especially behind reverse proxies like Render/Koyeb)
CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        'CSRF_TRUSTED_ORIGINS',
        'http://localhost:8000,http://127.0.0.1:8000,https://*.onrender.com,https://*.koyeb.app'
    ).split(',')
    if origin.strip()
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Local project applications
    'accounts.apps.AccountsConfig',
    'market.apps.MarketConfig',
    'moderation.apps.ModerationConfig',
    'core.apps.CoreConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # High-performance static files in production
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # Language selection and negotiation
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'core.context_processors.global_campus_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database Configuration
# Uses PostgreSQL if DATABASE_URL is set, otherwise defaults to SQLite for local development
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Custom User Model
AUTH_USER_MODEL = 'accounts.User'

# Authentication URLs
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'market:product_list'
LOGOUT_REDIRECT_URL = 'core:home'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization & Localization
# Target languages: English, Afaan Oromo (om), Amharic (am)
import django.conf.locale

EXTRA_LANG_INFO = {
    'om': {
        'bidi': False,
        'code': 'om',
        'name': 'Oromo',
        'name_local': 'Afaan Oromoo',
    },
    'am': {
        'bidi': False,
        'code': 'am',
        'name': 'Amharic',
        'name_local': 'አማርኛ',
    },
}
django.conf.locale.LANG_INFO.update(EXTRA_LANG_INFO)

LANGUAGE_CODE = 'en'

LANGUAGES = [
    ('en', 'English'),
    ('om', 'Afaan Oromoo'),
    ('am', 'አማርኛ'),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

TIME_ZONE = 'Africa/Addis_Ababa'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Whitenoise storage configuration
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Media files (User & Shop uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# File upload limits (maximum 4MB to prevent denial of service on free hosting)
DATA_UPLOAD_MAX_MEMORY_SIZE = 4 * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 4 * 1024 * 1024

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Business logic configuration
# Listings unconfirmed beyond this threshold are tagged stale
PRICE_STALE_DAYS = int(os.getenv('PRICE_STALE_DAYS', '7'))

# Production Security Headers
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
