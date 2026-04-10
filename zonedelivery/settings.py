from pathlib import Path
import os
from decouple import config, Csv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# Environment Detection
IS_RENDER = os.getenv('RENDER') == 'True'
IS_PRODUCTION = IS_RENDER or os.getenv('ENVIRONMENT') == 'production'

SECRET_KEY = config('SECRET_KEY', default='django-insecure-z!8xq%j2k9@p_x+f*v&h^d-c$e=r!t@u^&*(d%j^&*(')

DEBUG = config('DEBUG', default=True, cast=bool)

# Allowed Hosts Configuration
if IS_PRODUCTION:
    # Render production
    ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='delevaryzone-1.onrender.com,localhost,127.0.0.1', cast=Csv())
else:
    # Development (ngrok, localhost)
    ALLOWED_HOSTS = [
        'shan-nondecorative-timothy.ngrok-free.dev',
        'localhost',
        '127.0.0.1',
        '*.ngrok-free.dev',
        '*.ngrok.io',
    ]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'shop',
    'django_bootstrap5',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'zonedelivery.urls'

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
                'shop.context_processors.language_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'zonedelivery.wsgi.application'

# Database Configuration
if IS_RENDER:
    # Render Deployment with PostgreSQL
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME', default='zonedelivery_db'),
            'USER': config('DB_USER', default='postgres'),
            'PASSWORD': config('DB_PASSWORD', default=''),
            'HOST': config('DB_HOST', default='localhost'),
            'PORT': config('DB_PORT', default='5432'),
        }
    }
else:
    # Local Development with SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'bn'
TIME_ZONE = 'Asia/Dhaka'
USE_I18N = True
USE_TZ = True

# Language Support
LANGUAGES = [
    ('en', 'English'),
    ('bn', 'বাংলা'),
]

# Locale paths
LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# ============ SECURITY & HTTPS CONFIGURATION ============
if IS_PRODUCTION:
    # Production (Render)
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    CSRF_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    CSRF_COOKIE_SAMESITE = 'Lax'
    
    # CSRF Trusted Origins for Render
    csrf_origins = config('ALLOWED_HOSTS', default='localhost', cast=Csv())
    CSRF_TRUSTED_ORIGINS = [f'https://{host}' for host in csrf_origins]
else:
    # Development (ngrok, localhost)
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 0
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False
    SESSION_COOKIE_DOMAIN = '.ngrok-free.dev'
    CSRF_COOKIE_DOMAIN = '.ngrok-free.dev'
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SAMESITE = 'Lax'
    CSRF_COOKIE_SECURE = True
    CSRF_TRUSTED_ORIGINS = [
        'https://*.ngrok-free.dev',
        'http://*.ngrok-free.dev',
        'https://*.ngrok.io',
        'http://*.ngrok.io',
        'http://127.0.0.1:8000',
        'http://localhost:8000',
    ]

# Static & Media
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ============ GOOGLE MAPS API CONFIGURATION ============
GOOGLE_MAPS_API_KEY = config('GOOGLE_MAPS_API_KEY', default='AIzaSyAMu1dHt5cxLWaKH11uffQPDaOTozs__O8')