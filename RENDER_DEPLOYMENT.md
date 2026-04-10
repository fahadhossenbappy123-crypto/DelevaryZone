# ZoneDelivery - Render Deployment Guide

## Issues Fixed

The error `builder.sh: line 51: cd: /opt/render/project/src: No such file or directory` was caused by:
1. Missing `render.yaml` configuration
2. Missing `gunicorn` in requirements.txt
3. Django settings not configured for production

## What I've Done

1. Created `render.yaml` - Render's infrastructure configuration
2. Added `gunicorn` to requirements.txt
3. Created this deployment guide

## Setup Instructions

### Step 1: Update Django Settings for Production
Edit `zonedelivery/settings.py` and add this at the end to handle environment variables:

```python
# Production Settings for Render
import os

if not DEBUG:
    ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost').split(',')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    CSRF_TRUSTED_ORIGINS = [f"https://{host}" for host in ALLOWED_HOSTS]
```

### Step 2: Deploy on Render

1. **Connect GitHub Repository**
   - Go to [render.com](https://render.com)
   - Click "New +"
   - Select "Web Service"
   - Connect your GitHub repository: `https://github.com/fahadhossenbappy123-crypto/DeliveryZone`

2. **Auto-Deploy Configuration**
   - Render will automatically detect `render.yaml` and use it
   - The build commands will run in this order:
     - Install dependencies
     - Run migrations
     - Collect static files
   - Then start the server with gunicorn

3. **Set Environment Variables in Render Dashboard**
   ```
   ALLOWED_HOSTS: yourdomain.onrender.com
   SECRET_KEY: (generate a new secure key)
   DEBUG: False
   ```

### ⚠️ Important: Database Issue

**SQLite won't work on Render!** 

Render's filesystem is ephemeral (resets on redeploy). Your SQLite database will be lost.

**Solution: Use PostgreSQL**

1. Create a PostgreSQL database on Render
2. Add to requirements.txt:
   ```
   psycopg2-binary==2.9.9
   python-decouple==3.8
   ```

3. Update `settings.py`:
   ```python
   import os
   from decouple import config
   
   if os.getenv('RENDER'):
       DATABASES = {
           'default': {
               'ENGINE': 'django.db.backends.postgresql',
               'NAME': config('DB_NAME'),
               'USER': config('DB_USER'),
               'PASSWORD': config('DB_PASSWORD'),
               'HOST': config('DB_HOST'),
               'PORT': config('DB_PORT', '5432'),
           }
       }
   else:
       # Development (SQLite)
       DATABASES = {
           'default': {
               'ENGINE': 'django.db.backends.sqlite3',
               'NAME': BASE_DIR / 'db.sqlite3',
           }
       }
   ```

### Step 3: Push to GitHub

```bash
git add .
git commit -m "Add Render deployment configuration"
git push origin main
```

Render will automatically trigger a deploy!

## Monitoring

- **Logs**: View in Render dashboard → Select your service → Logs tab
- **Common Issues**:
  - `Module not found`: Check requirements.txt
  - `Database error`: Ensure PostgreSQL credentials in environment variables
  - `404 for static files`: Run `python manage.py collectstatic` locally to verify

## After Deployment

1. Run migrations on Render:
   - Go to service → Shell tab
   - Run: `python manage.py migrate`

2. Create superuser:
   - Run: `python manage.py createsuperuser`

3. Access your app at: `https://your-service-name.onrender.com`

