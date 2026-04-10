from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

SECRET_KEY = 'django-insecure-z!8xq%j2k9@p_x+f*v&h^d-c$e=r!t@u^&*(d%j^&*('

DEBUG = True

# Allow all hosts for development (ngrok, localhost, etc)
# For production, specify exact domains
# ALLOWED_HOSTS is defined in NGROK CONFIGURATION section below

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

# Database
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
# Geolocation API requires HTTPS (or localhost exception)
# NGROK provides HTTPS, so we enable secure flags
SECURE_SSL_REDIRECT = True  # ngrok provides HTTPS
SECURE_HSTS_SECONDS = 0  # Set to 31536000 in production

# Allow localhost and 127.0.0.1 for development
# For phone testing, use HTTPS (ngrok) or test from localhost
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False

# ============ NGROK CONFIGURATION ============
ALLOWED_HOSTS = [
    'shan-nondecorative-timothy.ngrok-free.dev',
    'localhost',
    '127.0.0.1',
    '*.ngrok-free.dev',  # Allow all ngrok-free subdomains
    '*.ngrok.io',        # Allow old ngrok domains too
]

# For testing with ngrok, configure session and CSRF cookies
# ngrok provides HTTPS, so secure cookies work properly
SESSION_COOKIE_DOMAIN = '.ngrok-free.dev'  # For ngrok-free service
CSRF_COOKIE_DOMAIN = '.ngrok-free.dev'     # For ngrok-free service
SESSION_COOKIE_SAMESITE = 'Lax'            # 'Lax' works better with redirects than 'None'
SESSION_COOKIE_SECURE = True               # HTTPS required (ngrok provides this)
CSRF_COOKIE_SAMESITE = 'Lax'               # 'Lax' for better compatibility
CSRF_COOKIE_SECURE = True                  # HTTPS required (ngrok provides this)
CSRF_TRUSTED_ORIGINS = [
    'https://*.ngrok-free.dev',   # ngrok-free service
    'http://*.ngrok-free.dev',
    'https://*.ngrok.io',         # older ngrok free service
    'http://*.ngrok.io',

    'http://127.0.0.1:8000',
    'http://localhost:8000',
]

# Optional: If using a specific ngrok domain instead, use:
# SESSION_COOKIE_DOMAIN = 'abcd1234.ngrok.io'  # Your specific ngrok URL
# CSRF_COOKIE_DOMAIN = 'abcd1234.ngrok.io'

# Static & Media
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ============ GOOGLE MAPS API CONFIGURATION ============
# Get your API key from: https://console.cloud.google.com
# Steps:
# 1. Create a new project
# 2. Enable: Maps JavaScript API, Places API, Directions API
# 3. Create an API key and restrict to HTTP referrers
# 4. Add your key below or use environment variable
import os
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', 'AIzaSyAMu1dHt5cxLWaKH11uffQPDaOTozs__O8')

# For development, you can also add it directly (not recommended for production!)
# GOOGLE_MAPS_API_KEY = 'AIzaSyD...'  # আপনার key এখানে যোগ করুন