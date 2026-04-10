# Render PostgreSQL Database Setup Guide

এই গাইড অনুসরণ করে Render এ PostgreSQL database তৈরি করুন এবং credentials সংগ্রহ করুন।

---

## 📋 Step 1: Render Dashboard এ যান এবং Database তৈরি করুন

### 1. Render Dashboard খুলুন
```
https://dashboard.render.com
```

### 2. নতুন PostgreSQL Database তৈরি করুন
- Dashboard এ "New +" ক্লিক করুন
- **"PostgreSQL"** নির্বাচন করুন
- এই তথ্য ভরুন:

| Field | Value |
|-------|-------|
| **Name** | `zonedelivery-db` |
| **Database** | `zonedelivery_db` |
| **User** | `postgres` |
| **Region** | যেখানে Web Service আছে সেখানেই |
| **PostgreSQL Version** | 15 (সর্বশেষ stable) |

### 3. Create Database ক্লিক করুন

⏳ 2-3 মিনিট অপেক্ষা করুন database তৈরি হতে।

---

## 🔑 Step 2: Database Credentials সংগ্রহ করুন

Database তৈরি হওয়ার পর আপনি একটি **"Info"** ট্যাব দেখবেন।

এখানে আপনি পাবেন:

```
Hostname: postgresql-xxxxx.c.render.com
Database: zonedelivery_db
Username: postgres
Password: xxxxxxxxxxxxxxxxxxxxxx
Port: 5432
External Database URL: postgresql://postgres:xxxxx@postgresql-xxxxx.c.render.com:5432/zonedelivery_db
```

**এই তথ্য গুলি কপি করে নিরাপদ জায়গায় রাখুন** (Password খুবই গুরুত্বপূর্ণ!)

---

## ⚙️ Step 3: Environment Variable সেটআপ করুন

### অপশন A: আপনার Web Service এ Environment Variable যোগ করুন

Web Service Dashboard এ যান → **Environment** ট্যাব

এই Variables যোগ করুন:

```
DB_NAME=zonedelivery_db
DB_USER=postgres
DB_PASSWORD=আপনার-PostgreSQL-password
DB_HOST=postgresql-xxxxx.c.render.com
DB_PORT=5432
RENDER=True
```

### অপশন B: Local Development এর জন্য .env ফাইল তৈরি করুন

আপনার project root এ `.env` ফাইল তৈরি করুন:

```properties
# Local Development - SQLite
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,*.ngrok-free.dev
GOOGLE_MAPS_API_KEY=your-api-key

# ঐচ্ছিক: Local এ PostgreSQL ব্যবহার করতে চাইলে
# DB_ENGINE=postgresql
# DB_NAME=zonedelivery_db
# DB_USER=postgres  
# DB_PASSWORD=your-password
# DB_HOST=localhost
# DB_PORT=5432
```

---

## 🚀 Step 4: Migrations চালান

### Web Service এ Shell এ যান (Render Dashboard)

1. আপনার Web Service নির্বাচন করুন
2. **"Shell"** ট্যাব ক্লিক করুন
3. এই কমান্ড চালান:

```bash
python manage.py migrate
```

আপনি দেখবেন:
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, shop
Running migrations:
  Applying migrations... OK
```

### Superuser তৈরি করুন (Admin)

একই Shell এ এই কমান্ড চালান:

```bash
python manage.py createsuperuser
```

এটি আপনাকে জিজ্ঞাসা করবে:
```
Username: admin
Email: your-email@example.com
Password: (টাইপ করুন)
Password (again): (আবার টাইপ করুন)
```

সফল হলে দেখবেন:
```
Superuser created successfully.
```

---

## 🎯 Step 5: Static Files Collect করুন

Shell এ এই কমান্ড চালান:

```bash
python manage.py collectstatic --no-input
```

---

## ✅ সবকিছু সম্পন্ন!

এখন আপনার app এ যান:

```
https://your-service-name.onrender.com
```

Admin panel এ login করুন:
```
https://your-service-name.onrender.com/admin/
```

**Username:** admin  
**Password:** আপনি যা তৈরি করেছেন

---

## 🆘 সমস্যা হলে

### সমস্যা: "could not connect to server"

**সমাধান:**
1. Database Hostname সঠিক কিনা চেক করুন
2. Password সঠিক কিনা verify করুন
3. Port 5432 সঠিক কিনা চেক করুন
4. Render Dashboard → Database → "Connections allowed from" সেকশন চেক করুন

### সমস্যা: "relation does not exist"

**সমাধান:**
```bash
python manage.py migrate
```
আবার চালান

### সমস্যা: Static files 404

**সমাধান:**
```bash
python manage.py collectstatic --no-input
```
আবার চালান

---

## 📊 Local Development এ PostgreSQL ব্যবহার করতে

যদি local এ PostgreSQL ব্যবহার করতে চান:

### 1. Install PostgreSQL
- ডাউনলোড করুন: https://www.postgresql.org/download/

### 2. Create Database
```bash
createdb zonedelivery_db
```

### 3. .env ফাইল আপডেট করুন
```properties
DB_ENGINE=postgresql
DB_NAME=zonedelivery_db
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
```

### 4. Migrate করুন
```bash
python manage.py migrate
```

---

## 🔐 নিরাপত্তা টিপস

⚠️ **কখনো এই তথ্য GitHub এ commit করবেন না:**
- Database Password
- SECRET_KEY
- API Keys

**ব্যবহার করুন:**
- `.env` ফাইল (local)
- Render Environment Variables (production)
- `.gitignore` এ `.env` যোগ করুন

---

**সবকিছু ঠিক থাকলে আপনার app এখন fully production-ready!** 🎉
