# Local Development Setup এবং Render Database Integration

## 🚀 Quick Start

### 1. Local .env ফাইল তৈরি করুন

Project root এ একটি `.env` ফাইল তৈরি করুন এবং এটি পেস্ট করুন:

```properties
# Django Settings
DEBUG=True
SECRET_KEY=django-insecure-z!8xq%j2k9@p_x+f*v&h^d-c$e=r!t@u^&*(d%j^&*(
ALLOWED_HOSTS=localhost,127.0.0.1,*.ngrok-free.dev
GOOGLE_MAPS_API_KEY=AIzaSyAMu1dHt5cxLWaKH11uffQPDaOTozs__O8

# Local Development - SQLite (default)
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# Security (Local)
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
```

> **⚠️ গুরুত্বপূর্ণ:** `.env` ফাইল কখনো GitHub এ commit করবেন না!

---

## 📦 Dependencies ইনস্টল করুন

```powershell
pip install -r requirements.txt
```

---

## 🗄️ Database Migrations চালান

Local development এর জন্য (SQLite ব্যবহার করছে):

```powershell
python manage.py migrate
```

এটি `db.sqlite3` তৈরি করবে।

---

## 👤 Superuser (Admin) তৈরি করুন

```powershell
python manage.py createsuperuser
```

Prompt এ ভরুন:
```
Username: admin
Email: admin@example.com
Password: (কোন password দিন)
Password (again): (আবার টাইপ করুন)
```

---

## 🌐 Local Server চালান

```powershell
python manage.py runserver
```

Access করুন:
- App: http://127.0.0.1:8000
- Admin: http://127.0.0.1:8000/admin/

---

## 🔄 Render Production এ Deploy করার পদক্ষেপ

### Step 1: Render এ PostgreSQL Database তৈরি করুন

বিস্তারিত গাইড দেখুন: [POSTGRESQL_SETUP.md](POSTGRESQL_SETUP.md)

### Step 2: Database Credentials সংগ্রহ করুন

Render Dashboard → PostgreSQL DB → Info ট্যাব থেকে:
- Hostname
- Database name
- Username
- Password

### Step 3: Render এ Environment Variables সেট করুন

Web Service Dashboard → Environment সেকশনে এই Variables যোগ করুন:

```
DEBUG=False
SECRET_KEY=your-new-secure-key-here
ALLOWED_HOSTS=your-service-name.onrender.com
GOOGLE_MAPS_API_KEY=AIzaSyAMu1dHt5cxLWaKH11uffQPDaOTozs__O8

# PostgreSQL Credentials (Render Database থেকে)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=zonedelivery_db
DB_USER=postgres
DB_PASSWORD=your-render-password
DB_HOST=postgresql-xxxxx.c.render.com
DB_PORT=5432

RENDER=True
```

### Step 4: Shell এ Migrations চালান

Render Dashboard:
1. Web Service নির্বাচন করুন
2. **Shell** ট্যাব ক্লিক করুন
3. এই কমান্ড চালান:

```bash
python manage.py migrate
```

### Step 5: Superuser তৈরি করুন

একই Shell এ:

```bash
python manage.py createsuperuser
```

### Step 6: Static Files Collect করুন

```bash
python manage.py collectstatic --no-input
```

---

## 🔗 Ngrok দিয়ে Phone Testing করুন

Local development এ phone থেকে test করতে:

### 1. Ngrok install করুন
```bash
pip install pyngrok
```

অথবা: https://ngrok.com/download

### 2. Ngrok টানেল শুরু করুন

```powershell
ngrok http 8000
```

You'll see:
```
Forwarding                    https://abcd1234.ngrok-free.dev -> http://127.0.0.1:8000
```

### 3. .env আপডেট করুন

```properties
ALLOWED_HOSTS=localhost,127.0.0.1,abcd1234.ngrok-free.dev
```

### 4. Server রিস্টার্ট করুন

```powershell
python manage.py runserver
```

### 5. Phone তে access করুন

Phone এর browser এ খুলুন:
```
https://abcd1234.ngrok-free.dev
```

---

## 📝 Common Commands রেফারেন্স

| কমান্ড | কাজ |
|--------|------|
| `python manage.py runserver` | Local server চালান |
| `python manage.py makemigrations` | Model changes detect করুন |
| `python manage.py migrate` | Database changes apply করুন |
| `python manage.py createsuperuser` | Admin user তৈরি করুন |
| `python manage.py collectstatic` | Static files collect করুন |
| `python manage.py shell` | Django shell খুলুন |

---

## 🆘 সমস্যা সমাধান

### সমস্যা: "No module named decouple"

```powershell
pip install python-decouple
```

### সমস্যা: "No module named psycopg2"

PostgreSQL ব্যবহার করলে:

```powershell
pip install psycopg2-binary
```

### সমস্যা: "SECRET_KEY 404" errors

`settings.py` এ environment variable সেটআপ চেক করুন।

### সমস্যা: "ALLOWED_HOSTS error"

`.env` ফাইলে `ALLOWED_HOSTS` সঠিক কিনা চেক করুন।

---

## ✅ Checklist - Deploy হওয়ার আগে

- [ ] Local এ সব test করেছেন
- [ ] `.env` ফাইল `.gitignore` এ আছে
- [ ] `db.sqlite3` `.gitignore` এ আছে
- [ ] GitHub এ সব code push করেছেন
- [ ] Render PostgreSQL database তৈরি করেছেন
- [ ] Render Environment Variables সেট করেছেন
- [ ] `render.yaml` সঠিক আছে

---

## 🎉 সবকিছু সম্পন্ন হলে

আপনার production app:
```
https://your-service-name.onrender.com
```

Admin panel:
```
https://your-service-name.onrender.com/admin/
```

---

**কোন সমস্যা হলে POSTGRESQL_SETUP.md দেখুন!** 📚
