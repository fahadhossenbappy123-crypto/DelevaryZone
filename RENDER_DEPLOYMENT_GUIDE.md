# 🚀 Render এ Deploy করার Guide

আপনার ZoneDelivery project কে Render এ deploy করার জন্য complete step-by-step guide।

## Step 1: Render এ Account Create করুন
1. [render.com](https://render.com) এ যান
2. GitHub account দিয়ে sign up করুন
3. Dashboard এ যান

## Step 2: আপনার GitHub Repository Connect করুন
1. Render Dashboard → "New +"
2. "Web Service" select করুন
3. আপনার GitHub repository select করুন
4. Connect করুন

## Step 3: Web Service Configuration

### Basic Settings
- **Name**: `zonedelivery` (অথবা আপনার পছন্দের name)
- **Environment**: `Python 3`
- **Region**: `Singapore` (Bangladesh এর কাছাকাছি) অথবা `Frankfurt`
- **Branch**: `main` (অথবা আপনার deployment branch)

### Build Command
```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

### Start Command
```bash
gunicorn zonedelivery.wsgi:application --bind 0.0.0.0:$PORT
```

## Step 4: Environment Variables Set করুন

Render Dashboard → Web Service → Environment এ যান এবং নিম্নলিখিত variables add করুন:

### **REQUIRED Variables (অবশ্যই set করতে হবে)**

| Variable | Value | Example |
|----------|-------|---------|
| `SECRET_KEY` | একটি strong random key | `django-insecure-abc123...xyz` |
| `DATABASE_URL` | আপনার PostgreSQL URL | `postgresql://user:pass@host:5432/db` |
| `ALLOWED_HOSTS` | আপনার domain names | `zonedelivery.onrender.com,localhost` |

### **OPTIONAL Variables**

| Variable | Value | Default |
|----------|-------|---------|
| `GOOGLE_MAPS_API_KEY` | আপনার Google Maps API Key | (empty) |
| `EMAIL_HOST_USER` | আপনার email | (empty) |
| `EMAIL_HOST_PASSWORD` | Email password/app password | (empty) |
| `CSRF_TRUSTED_ORIGINS` | CSRF trusted domains | `https://your-domain.onrender.com` |
| `DEBUG` | `False` (production) | `False` |

## Step 5: PostgreSQL Database Create করুন

### Option A: Render এ PostgreSQL Create করুন (Recommended)

1. Render Dashboard → "New +"
2. "PostgreSQL" select করুন
3. Fill করুন details:
   - **Name**: `zonedelivery-db`
   - **Database**: `zonedelivery_db`
   - **User**: `zonedelivery_user`
   - **Region**: Web service এর same region
4. Create করুন

5. Database created হলে, **DATABASE_URL** copy করুন
6. আপনার Web Service এ এই URL paste করুন `DATABASE_URL` environment variable এ

### Option B: External PostgreSQL Database ব্যবহার করুন
- Direct PostgreSQL URL আপনার `DATABASE_URL` environment variable এ set করুন

## Step 6: Django Migrations Run করুন

Deploy হওয়ার পর, migrations manually run করতে হতে পারে:

```bash
python manage.py migrate
```

এটি Render এ করতে পারেন:
1. Web Service settings এ যান
2. "Shell" option এ ক্লিক করুন (যদি available থাকে)
3. Command run করুন: `python manage.py migrate`

অথবা Build command এ already আছে।

## Step 7: Verify করুন

1. Render Dashboard এ আপনার Web Service এর logs দেখুন
2. আপনার domain এ visit করুন: `https://zonedelivery.onrender.com`
3. যদি কোনো error থাকে, logs এ check করুন

---

## 🔑 SECRET_KEY Generate করুন

Django secret key generate করতে, local এ run করুন:

```bash
python manage.py shell
```

তারপর:
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

Output: একটি long random string, এটি **SECRET_KEY** variable এ paste করুন।

---

## 🗄️ DATABASE_URL কোথা থেকে পাবেন?

**যদি Render এ PostgreSQL create করেছেন:**
1. PostgreSQL database detail page এ যান
2. "Connections" section এ "External Database URL" খুঁজুন
3. সম্পূর্ণ URL copy করুন

**Format**: `postgresql://username:password@hostname:5432/database_name`

---

## 🔐 Email Configuration (Optional)

যদি email functionality ব্যবহার করতে চান:

### Gmail এর জন্য:
1. [Google Account Security](https://myaccount.google.com/security) এ যান
2. "App Passwords" enable করুন
3. Email app password generate করুন
4. Render environment variables এ set করুন:
   - `EMAIL_HOST_USER`: আপনার gmail address
   - `EMAIL_HOST_PASSWORD`: generated app password

---

## ⚠️ Important Notes

1. **SECRET_KEY**: প্রতিটি environment এর জন্য unique হওয়া উচিত
2. **DEBUG**: Production এ সবসময় `False` রাখুন
3. **ALLOWED_HOSTS**: আপনার actual domain name set করুন
4. **Database Backups**: নিয়মিত database backup নিন
5. **Static Files**: WhiteNoise automatically handle করে (.venv require)

---

## 🐛 Troubleshooting

### 1. "ModuleNotFoundError" Error
- `requirements.txt` update করেছেন কিনা check করুন
- `pip freeze > requirements.txt` run করুন locally

### 2. "No such table" Error
- Migrations নি run করেননি
- Manual থেকে run করুন অথবা build command এ check করুন

### 3. Static Files নেই
- Run করুন: `python manage.py collectstatic --noinput`
- WhiteNoise middleware activate আছে কিনা check করুন

### 4. Database Connection Error
- DATABASE_URL correct কিনা check করুন
- Database host/port accessible কিনা verify করুন

### 5. Email নেই
- Email settings correct কিনা check করুন
- Gmail app password use করছেন কিনা verify করুন

---

## 📚 Environment Variables Summary

```bash
# Security
SECRET_KEY=your-secret-key-here

# Database
DATABASE_URL=postgresql://user:pass@host:5432/db

# Hosts
ALLOWED_HOSTS=zonedelivery.onrender.com,localhost

# APIs (Optional)
GOOGLE_MAPS_API_KEY=your-api-key

# CSRF
CSRF_TRUSTED_ORIGINS=https://zonedelivery.onrender.com

# Email (Optional)
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

---

## ✅ Deploy Success Checklist

- [ ] GitHub repository pushed
- [ ] Render Web Service created
- [ ] PostgreSQL database connected
- [ ] All environment variables set
- [ ] Build और start commands correct
- [ ] Migrations successful
- [ ] Static files working
- [ ] Admin panel accessible at `/admin/`
- [ ] Custom pages loading properly

---

Happy Deploying! 🎉
