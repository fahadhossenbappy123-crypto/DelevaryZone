# Render PostgreSQL Credentials সংগ্রহের ধাপ-দর-ধাপ গাইড

## 📸 Visual Guide - Render Dashboard এ

### Step 1: Dashboard এ যান
```
https://dashboard.render.com
```

### Step 2: বাম দিকের Menu এ "Databases" ক্লিক করুন

আপনি দেখবেন আপনার সব databases এর তালিকা।

### Step 3: আপনার Database নির্বাচন করুন

`zonedelivery-db` খুঁজুন এবং ক্লিক করুন।

---

## 🔑 Step 4: Credentials দেখুন এবং কপি করুন

Database detail page এ যাবেন। এখানে একটি **Info** সেকশন আছে।

এখানে আপনি পাবেন:

### A. Hostname
```
postgresql-xxxxx.c.render.com
```
✅ এটি কপি করুন এবং পাস্ট করুন: `DB_HOST`

### B. Database
```
zonedelivery_db
```
✅ এটি কপি করুন এবং পাস্ট করুন: `DB_NAME`

### C. User
```
postgres
```
✅ এটি কপি করুন এবং পাস্ট করুন: `DB_USER`

### D. Password
```
xxxxxxxxxxxxxxxxxxxxxxxx
```
✅ এটি কপি করুন এবং পাস্ট করুন: `DB_PASSWORD`  
⚠️ এই পাসওয়ার্ড খুবই গুরুত্বপূর্ণ, নিরাপদ জায়গায় রাখুন!

### E. Port
```
5432
```
✅ এটি সাধারণত সবসময় `5432` থাকে

### F. Internal Database URL
```
postgresql://postgres:xxxxxxx@postgresql-xxxxx.c.render.com:5432/zonedelivery_db
```
✅ এটি reference এর জন্য

---

## 📋 Step 5: Render Web Service এ Environment Variables সেট করুন

### যেখানে যেতে হবে:

1. **Dashboard** → আপনার Web Service নির্বাচন করুন (যেটা code deploy করছে)
2. **Settings** ট্যাব খুলুন
3. **Environment** সেকশন দেখবেন

### এই Variables যোগ করুন:

#### উপরের credentials থেকে আসা:

```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=zonedelivery_db
DB_USER=postgres
DB_PASSWORD=xxxxxxxxxxxxxxxxxxxxxxxx (কপি করা password)
DB_HOST=postgresql-xxxxx.c.render.com
DB_PORT=5432
```

#### অন্যান্য Important Variables:

```
RENDER=True
SECRET_KEY=আপনার-নতুন-দীর্ঘ-random-string
DEBUG=False
ALLOWED_HOSTS=your-service-name.onrender.com,www.your-service-name.onrender.com
GOOGLE_MAPS_API_KEY=AIzaSyAMu1dHt5cxLWaKH11uffQPDaOTozs__O8
```

---

## ✅ Variable যোগ করার পদ্ধতি (Render Dashboard)

### প্রতিটি Variable এর জন্য:

1. **"Add Environment Variable"** ক্লিক করুন
2. **Key** ফিল্ডে variable name দিন (e.g., `DB_HOST`)
3. **Value** ফিল্ডে মান দিন
4. **"Save"** ক্লিক করুন

Render স্বয়ংক্রিয়ভাবে service রিডিপ্লয় করবে।

---

## 🚀 Step 6: Deploy এবং Migration চালান

### Deploy সম্পূর্ণ হওয়ার জন্য অপেক্ষা করুন

Render Dashboard এ আপনার service এর **Deploy** লগ দেখুন। সবুজ checkpoint ✓ দেখা যাবে।

### Shell এ Migration চালান

একবার deploy সম্পন্ন হলে:

1. **Shell** ট্যাব ক্লিক করুন (আপনার Web Service পেজে)
2. এই কমান্ড চালান:

```bash
python manage.py migrate
```

আপনি দেখবেন:
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, shop, ...
Running migrations:
  Applying migrations... OK
```

### Superuser তৈরি করুন

একই Shell এ:

```bash
python manage.py createsuperuser
```

প্রম্পট এ ভরুন:
```
Username: admin
Email: your-email@example.com
Password: (শক্তিশালী password বেছে নিন)
Password (again): (আবার টাইপ করুন)
```

---

## 🎯 সফল হলে আপনি এখন এই লোকেশনে access করতে পারবেন:

```
https://your-service-name.onrender.com/admin/
```

**Username:** admin  
**Password:** আপনি যা সেট করেছেন

---

## 🆘 ট্রাবলশুটিং

### সমস্যা: "could not connect to server"

✅ **সমাধান:**
1. Credentials সঠিক কপি হয়েছে কিনা চেক করুন
2. Database এখনও Creating থাকতে পারে (5-15 মিনিট সময় লাগতে পারে)
3. Password এ special characters আছে কিনা দেখুন

### সমস্যা: Migration চলছে না

✅ **সমাধান:**
1. Shell এ কমান্ড আবার চালান
2. Web Service এর logs দেখুন
3. DB_HOST, DB_NAME সঠিক কিনা চেক করুন

### সমস্যা: "relation does not exist"

✅ **সমাধান:**
```bash
python manage.py migrate --run-syncdb
```

---

## 📸 Screenshot সম্ভাব্য Layout

```
┌─ Render Dashboard ──────────────────────┐
│                                         │
│ [Databases] ← Click here               │
│                                         │
│ ┌─ PostgreSQL Databases ──────┐        │
│ │ □ zonedelivery-db ← Click   │        │
│ └─────────────────────────────┘        │
│                                         │
│ ┌─ Info ──────────────────────────┐    │
│ │ Hostname: postgresql-x...       │    │
│ │ Database: zonedelivery_db       │    │
│ │ User: postgres                  │    │
│ │ Password: xxxxxxxxxxxx          │    │
│ │ Port: 5432                      │    │
│ └──────────────────────────────────┘    │
│                                         │
└─────────────────────────────────────────┘
```

---

## ✨ সবকিছু করা হলে

আপনার app এখন fully production-ready with PostgreSQL! 🎉

- ✅ Local development: SQLite
- ✅ Production (Render): PostgreSQL
- ✅ Environment variables configured
- ✅ Database migrations done
- ✅ Admin user created

---

**Additional Help:** 
- [LOCAL_SETUP.md](LOCAL_SETUP.md) - Local development গাইড
- [POSTGRESQL_SETUP.md](POSTGRESQL_SETUP.md) - PostgreSQL setup বিস্তারিত
- [DEPLOY_GUIDE.md](DEPLOY_GUIDE.md) - সম্পূর্ণ deployment গাইড
