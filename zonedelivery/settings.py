from pathlib import Path
import os
from decouple import config, Csv

# Conditional import for dj-database-url
try:
    import dj_database_url
except ImportError:
    dj_database_url = None

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# Environment Detection
IS_RENDER = os.getenv('RENDER') == 'True'
IS_PRODUCTION = IS_RENDER or os.getenv('ENVIRONMENT') == 'production'

# Render এ কোন environment variable add করতে হবে না - সব default values built-in আছে
SECRET_KEY = config('SECRET_KEY', default='django-insecure-zonedelivery-render-deployment-key-2024-secure')

DEBUG = config('DEBUG', default=False if IS_PRODUCTION else True, cast=bool)

# Allowed Hosts Configuration
if IS_PRODUCTION:
    # Render production - accept common Render domains with defaults built-in
    render_hosts = [
        'delevaryzone-1.onrender.com',
        'deleveryzone.onrender.com',
        'zonedelivery.onrender.com',
        'localhost',
        '127.0.0.1',
    ]
    # Try to read from environment, else use defaults above
    env_hosts = os.getenv('ALLOWED_HOSTS', '')
    if env_hosts:
        render_hosts = env_hosts.split(',')
    ALLOWED_HOSTS = render_hosts
else:
    # Development (ngrok, localhost)
    ALLOWED_HOSTS = [
        'delevaryzone-1.onrender.com',
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

# ============ CACHING CONFIGURATION ============
redis_url = os.getenv('REDIS_URL')
if IS_PRODUCTION and redis_url:
    # Production with Redis
    try:
        CACHES = {
            'default': {
                'BACKEND': 'django_redis.cache.RedisCache',
                'LOCATION': redis_url,
                'OPTIONS': {
                    'CLIENT_CLASS': 'django_redis.client.DefaultClient',
                    'CONNECTION_POOL_KWARGS': {'max_connections': 50, 'retry_on_timeout': True},
                    'SOCKET_CONNECT_TIMEOUT': 5,
                    'SOCKET_TIMEOUT': 5,
                    'COMPRESSOR': 'django_redis.compressors.zlib.ZlibCompressor',
                }
            }
        }
    except Exception as e:
        # Fallback to database cache if Redis fails
        CACHES = {
            'default': {
                'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
                'LOCATION': 'django_cache_table',
            }
        }
else:
    # Development or no Redis - use appropriate cache backend
    if IS_PRODUCTION:
        # Production without Redis - use database cache
        CACHES = {
            'default': {
                'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
                'LOCATION': 'django_cache_table',
            }
        }
    else:
        # Development - use local memory cache
        CACHES = {
            'default': {
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
                'LOCATION': 'unique-snowflake',
                'TIMEOUT': 300,
            }
        }

# Session caching - use database for production without Redis
if IS_PRODUCTION and not redis_url:
    SESSION_ENGINE = 'django.contrib.sessions.backends.db'
else:
    SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
    SESSION_CACHE_ALIAS = 'default'

SESSION_COOKIE_AGE = 1209600  # 2 weeks

# Database Configuration
# All database settings from environment variables (safe for production)
DATABASE_URL = os.getenv('DATABASE_URL')

if DATABASE_URL and dj_database_url:
    # Use Render's automatic DATABASE_URL if available
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_health_checks=True,
            conn_max_age=600,
        )
    }
else:
    # Fallback to manual configuration from environment
    db_engine = os.getenv('DB_ENGINE', 'django.db.backends.sqlite3')
    
    if 'postgresql' in db_engine:
        # PostgreSQL configuration
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': os.getenv('DB_NAME', 'zonedelivery_db'),
                'USER': os.getenv('DB_USER', 'postgres'),
                'PASSWORD': os.getenv('DB_PASSWORD', ''),
                'HOST': os.getenv('DB_HOST', 'localhost'),
                'PORT': os.getenv('DB_PORT', '5432'),
                'CONN_MAX_AGE': 600,
                'OPTIONS': {
                    'connect_timeout': 10,
                    'sslmode': 'require' if IS_PRODUCTION else 'disable',
                }
            }
        }
    else:
        # SQLite (Local Development)
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
# Render এ কোন environment variable add করতে হবে না - সব default আছে
if IS_PRODUCTION:
    # Production (Render) - সব built-in defaults এ কাজ করবে
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
    
    # CSRF Trusted Origins for Render with built-in defaults
    csrf_hosts = os.getenv('ALLOWED_HOSTS', 'delevaryzone-1.onrender.com,localhost,127.0.0.1').split(',')
    CSRF_TRUSTED_ORIGINS = [f'https://{host.strip()}' for host in csrf_hosts] + [f'http://{host.strip()}' for host in csrf_hosts]
    
    # Handle proxy headers from Render
    SECURE_PROXY_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
else:
    # Development (ngrok, localhost)
    SECURE_SSL_REDIRECT = False
    SECURE_HSTS_SECONDS = 0
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SAMESITE = 'Lax'
    CSRF_COOKIE_SECURE = False
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
# Render এ কোন environment variable set করতে হবে না - default API key built-in আছে
GOOGLE_MAPS_API_KEY = config('GOOGLE_MAPS_API_KEY', default='AIzaSyAMu1dHt5cxLWaKH11uffQPDaOTozs__O8')

# ============ PERFORMANCE OPTIMIZATION ============
# Use atomic database transactions for better performance
ATOMIC_REQUESTS = IS_PRODUCTION

# Optimize queries in templates
if IS_PRODUCTION:
    # Use cached templates
    TEMPLATES[0]['OPTIONS']['loaders'] = [
        ('django.template.loaders.cached.Loader', [
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ]),
    ]

# Logging for production monitoring
LOGGING = {
    'version': 1,
    'disable_existing_loggers': not DEBUG,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'WARNING' if IS_PRODUCTION else 'INFO',
        },
        'shop': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}

# Optimize ORM queries
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5 MB
