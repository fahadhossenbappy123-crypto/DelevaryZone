# Render Web Service - Environment Variables

এই environment variables গুলি আপনার Render Web Service Dashboard এ add করুন।

---

## 📝 যা করবেন:

1. Render Dashboard → আপনার Web Service নির্বাচন করুন
2. **Settings** ট্যাব খুলুন
3. **Environment** সেকশনে নিচের variables যোগ করুন

---

## 🔧 Environment Variables - Complete List

### **Core Django Settings** (Required)

```
DEBUG=False
SECRET_KEY=আপনার-নতুন-secure-secret-key-এখানে-লিখুন
ALLOWED_HOSTS=your-service-name.onrender.com,www.your-service-name.onrender.com
```

---

### **PostgreSQL Database Configuration** (Required)

Render Database Details থেকে নিন (Info ট্যাব):

```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=zonedelivery_db
DB_USER=postgres
DB_PASSWORD=আপনার-PostgreSQL-password-এখানে
DB_HOST=postgresql-xxxxx.c.render.com
DB_PORT=5432
```

---

### **Google Maps API** (Required যদি geolocation feature ব্যবহার করছেন)

```
GOOGLE_MAPS_API_KEY=AIzaSyAMu1dHt5cxLWaKH11uffQPDaOTozs__O8
```

---

### **Render Detection** (Required)

```
RENDER=True
```

---

### **Security Settings** (Optional কিন্তু সুপারিশকৃত)

```
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
```

---

### **Email Configuration** (Optional)

```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

---

## 📋 Quick Copy-Paste Format

আপনি প্রতিটি variable একবারে add করতে পারেন:

```
DEBUG=False
SECRET_KEY=django-insecure-বা-নতুন-শক্তিশালী-key
ALLOWED_HOSTS=your-service-name.onrender.com
GOOGLE_MAPS_API_KEY=AIzaSyAMu1dHt5cxLWaKH11uffQPDaOTozs__O8
RENDER=True
DB_ENGINE=django.db.backends.postgresql
DB_NAME=zonedelivery_db
DB_USER=postgres
DB_PASSWORD=আপনার-db-password
DB_HOST=postgresql-xxxxx.c.render.com
DB_PORT=5432
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

---

## ⚠️ গুরুত্বপূর্ণ Information:

| Variable | কোথা থেকে পাবেন | উদাহরণ |
|----------|-----------------|---------|
| `DB_PASSWORD` | Render PostgreSQL Database > Info tab | `xxxxxxxxxxxx` |
| `DB_HOST` | Render PostgreSQL Database > Info tab | `postgresql-xxxxx.c.render.com` |
| `ALLOWED_HOSTS` | আপনার Web Service এর নাম | `myapp.onrender.com` |
| `SECRET_KEY` | নতুন strong key generate করুন | `django-insecure-...` |
| `GOOGLE_MAPS_API_KEY` | আপনার API key | `AIzaSy...` |

---

## 🔐 Security Tips:

✅ **Strong SECRET_KEY generate করতে Python shell এ:**

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

❌ **কখনো করবেন না:**
- GitHub এ credentials push করবেন না
- Example values দিয়ে deploy করবেন না
- Production এ DEBUG=True রাখবেন না

---

## ✅ Add করার ধাপ:

1. **Environment** সেকশনে "Add Environment Variable" ক্লিক করুন
2. **Key** field এ variable name দিন (e.g., `DEBUG`)
3. **Value** field এ মান দিন (e.g., `False`)
4. **Save** ক্লিক করুন
5. প্রতিটি variable এর জন্য repeat করুন

---

## 📊 সব Variable একসাথে Add করলে:

Render automatically আপনার Web Service রিডিপ্লয় করবে।

**Status Check:**
- Green checkmark ✓ = সফল
- Red X ✗ = কোন মিস্টেক আছে

---

## 🚀 Add করার পরবর্তী ধাপ:

1. Web Service deployment complete হওয়ার জন্য অপেক্ষা করুন
2. **Shell** ট্যাবে যান
3. এই কমান্ড চালান:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --no-input
```

---

**Ready! সব variables add করুন এবং deploy করুন।** 🚀
