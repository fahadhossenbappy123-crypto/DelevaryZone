# ✅ Render Deployment - Complete Checklist

## আপনার deployment কেন fail হচ্ছে এবং কিভাবে fix করবেন

---

## 🔴 Problem কী?

Build succeed কিন্তু deployment fail হচ্ছে মানে:
- ✅ Code download হয়েছে
- ✅ Dependencies install হয়েছে  
- ✅ Database migrations run হয়েছে
- ✅ Static files collect হয়েছে
- ❌ **কিন্তু gunicorn server start হতে পারছে না**

### এর কারণ:
- `SECRET_KEY` environment variable set না হওয়া
- `ALLOWED_HOSTS` production domain এ set না হওয়া
- Database credentials set না হওয়া (migrations fail করে)

---

## 🛠️ Solution - Render Dashboard এ যা করবেন

### Step 1: আপনার Web Service এ যান

1. **[Render Dashboard](https://dashboard.render.com)** খুলুন
2. বাম দিক থেকে **"Web Services"** ক্লিক করুন
3. আপনার `zonedelivery` service নির্বাচন করুন

---

### Step 2: Environment Variables Add করুন

1. Service detail page এ যান
2. **"Environment"** সেকশন খুঁজুন
3. নিচের সব variables যোগ করুন:

#### 🔑 **Critical Variables** (MUST HAVE)

```
DEBUG=False
RENDER=True
SECRET_KEY=your-super-long-random-secure-key-here-minimum-50-chars
ALLOWED_HOSTS=zonedelivery.onrender.com,www.zonedelivery.onrender.com
DJANGO_SETTINGS_MODULE=zonedelivery.settings
```

#### 🗄️ **Database Variables** (যদি PostgreSQL ব্যবহার করছেন)

```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=zonedelivery_db
DB_USER=postgres
DB_PASSWORD=your-postgres-password-from-render-database
DB_HOST=postgresql-xxxxx.c.render.com
DB_PORT=5432
```

#### 📍 **Google Maps API** (Optional)

```
GOOGLE_MAPS_API_KEY=AIzaSyAMu1dHt5cxLWaKH11uffQPDaOTozs__O8
```

#### 🔒 **Security Variables** (Recommended)

```
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
```

---

### Step 3: Database Connection করুন (যদি PostgreSQL হয়)

যদি PostgreSQL database Render এ create করছেন:

1. Dashboard এ **"Databases"** যান
2. **"Create"** >> **"PostgreSQL"** নির্বাচন করুন
3. Database create হওয়ার পর:
   - **Info** tab খুলুন
   - Hostname, Database, User, Password, Port copy করুন
   - উপরের environment variables এ পেস্ট করুন

---

### Step 4: Deploy করুন

#### Option A - Automatic (Recommended)
```bash
git push origin main
# Render automatically redeploy করবে
```

#### Option B - Manual Redeploy Render Dashboard থেকে
1. Service page এ যান
2. **"Manual Deploy"** >> **"Deploy latest commit"** ক্লিক করুন

---

## 📋 Environment Variable Reference

আপনার current domain এ আপডেট করুন:

| Variable | Value | Example |
|----------|-------|---------|
| `ALLOWED_HOSTS` | আপনার Render domain | `myapp.onrender.com,www.myapp.onrender.com` |
| `SECRET_KEY` | 50+ character random string | `django-insecure-abc123xyz...` |
| `DB_HOST` | PostgreSQL hostname | `postgresql-xxxxx.c.render.com` |
| `DB_PASSWORD` | Your database password | `(ভাবি নিজের password)` |

---

## 🐛 Debug করার জন্য

যদি এর পরেও fail হয়, এই steps follow করুন:

### 1. Build Logs দেখুন
```
Dashboard → Your Service → Logs
```

### 2. Common Errors:

❌ **`No such file or directory`**
- সমাধান: render.yaml এ path check করুন
- আমরা ইতিমধ্যে fix করেছি ✅

❌ **`psycopg2` error**
- সমাধান: requirements.txt এ `psycopg2-binary==2.9.9` আছে কিনা check করুন ✅

❌ **`SECRET_KEY not set`**
- সমাধান: Environment এ `SECRET_KEY` add করুন ✅

❌ **`ALLOWED_HOSTS` error**
- সমাধান: আপনার actual Render domain দিয়ে update করুন ✅

---

## ✨ Quick Deploy Script

আপনার local terminal এ এই commands run করুন:

```bash
# 1. সব কিছু commit করুন
git add .
git commit -m "Fix Render deployment issues"
git push origin main

# 2. অপেক্ষা করুন - Render automatic deploy করবে
# Dashboard নিয়মিত watch করুন
```

---

## 📞 Still Not Working?

যদি এর পরেও issue থাকে, চেক করুন:

1. ✅ render.yaml এ সব variables স্থির আছে
2. ✅ requirements.txt এ gunicorn আছে
3. ✅ Render Dashboard এ সব environment variables সেট হয়েছে
4. ✅ PostgreSQL database Render এ create করেছেন (যদি ব্যবহার করছেন)
5. ✅ SECRET_KEY এবং DATABASE credentials সঠিক

---

## 🎯 Success Signs

Deploy successful হলে:
- ✅ Build log এ কোনো error নেই
- ✅ Service status "Live" দেখাচ্ছে
- ✅ আপনার domain এ app accessible হচ্ছে
- ✅ Database connection working করছে

---

Last Updated: April 10, 2026
