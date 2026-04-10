# 🔍 How to Debug Render Deployment Issues

## Where to Find Logs

### 1. **Render Dashboard Logs** (সবচেয়ে গুরুত্বপূর্ণ)

**Path:**
```
https://dashboard.render.com/ 
→ Web Services 
→ zonedelivery (আপনার service) 
→ Logs tab
```

---

## 📊 Deployment Stages & Common Issues

### **Stage 1: Code Download**
```
Starting build...
Cloning repository...
```
✅ এখানে usually কোনো সমস্যা হয় না।

---

### **Stage 2: Build**

#### Build Command:
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --no-input
```

#### Common Issues:

**❌ Error: `No module named 'xyz'`**
```
ModuleNotFoundError: No module named 'psycopg2'
```
**সমাধান:**
- requirements.txt এ সব package আছে কিনা check করুন
- `pip freeze > requirements.txt` run করুন locally
- Git push করুন

---

**❌ Error: `django.db.utils.OperationalError`** (Database connection error)
```
OperationalError: could not translate host name "postgresql-xxxxx.c.render.com" to address
```
**সমাধান:**
- DB_HOST এ correct hostname আছে কিনা check করুন
- PostgreSQL database Render এ accessible আছে কিনা check করুন

---

**❌ Error: `KeyError 'SECRET_KEY'` বা `SECRET_KEY not found`**
```
KeyError: 'SECRET_KEY'
```
**সমাধান:**
- Render Dashboard → Environment → SECRET_KEY add করুন

---

#### ✅ Successful Build Output:
```
Installing dependencies...
✓ All dependencies installed
Running migrations...
✓ Migrations completed
Collecting static files...
✓ Static files collected successfully
Build completed in XX seconds
```

---

### **Stage 3: Deployment** (এখানেই সবচেয়ে বেশি fail হয়)

#### Deployment Command:
```bash
gunicorn zonedelivery.wsgi:application --timeout 30 --workers 2
```

#### Common Issues:

**❌ Error: `Process exited with status code 1`**
```
Exit status 1
Gunicorn unable to start
```
**Possible Reasons:**
1. SECRET_KEY missing
2. ALLOWED_HOSTS wrong
3. Database connection failing
4. DJANGO_SETTINGS_MODULE wrong

**সমাধান:**
```
1. Render Dashboard → Environment
2. এই variables add করুন:
   - DEBUG=False
   - RENDER=True
   - SECRET_KEY=[strong key]
   - ALLOWED_HOSTS=zonedelivery.onrender.com
   - DJANGO_SETTINGS_MODULE=zonedelivery.settings
3. Manual Deploy করুন
```

---

**❌ Error: `Address already in use`**
```
Error: Address already in use (port 10000)
```
**সমাধান:**
- Render automatically assign করে port
- আমাদের startCommand ঠিক আছে
- আর একবার Manual Deploy করুন

---

**❌ Error: `DisallowedHost at /`**
```
DisallowedHost at /
Invalid HTTP_HOST header: 'xyz.onrender.com'
```
**সমাধান:**
```
ALLOWED_HOSTS=zonedelivery.onrender.com
অথবা যদি multiple domains
ALLOWED_HOSTS=zonedelivery.onrender.com,www.zonedelivery.onrender.com
```

---

## 🛠️ How to Read Logs Properly

### **Build Phase Logs**

```
# ✅ OK
Starting build...
[build] Creating build environment
[build] $ pip install -r requirements.txt
Collecting Django==5.1.7
...
Successfully installed Django-5.1.7

# ⚠️ Watch for errors
ERROR: Could not find version that satisfies the requirement
ERROR: No matching distribution found
```

### **Deployment Phase Logs**

```
# ✅ OK
Starting service...
[init] $ python manage.py migrate
Operations to perform:
✓ Apply all migrations
[init] $ python manage.py collectstatic --no-input
...
Starting gunicorn
[app] INFO spawned uWSGI worker 1
[app] INFO spawned uWSGI worker 2
Listening on 0.0.0.0:10000

# ❌ FAIL
OperationalError: could not connect to server
CRITICAL: SIGTERM received, shutting down
DisallowedHost: 'xyz.onrender.com' is not in ALLOWED_HOSTS
```

---

## 📋 Complete Debugging Checklist

### When Build Succeeds but Deploy Fails:

- [ ] `DEBUG=False` - Render এ set করেছেন?
- [ ] `RENDER=True` - Render এ set করেছেন?
- [ ] `SECRET_KEY` - Valid, long string এ set করেছেন?
- [ ] `ALLOWED_HOSTS` - আপনার actual Render domain এ set করেছেন?
- [ ] `DJANGO_SETTINGS_MODULE=zonedelivery.settings` - Render এ set করেছেন?
- [ ] Database (যদি PostgreSQL):
  - [ ] PostgreSQL database Render এ create করেছেন?
  - [ ] `DB_HOST` সঠিক hostname এ set করেছেন?
  - [ ] `DB_USER` সঠিক username এ set করেছেন?
  - [ ] `DB_PASSWORD` সঠিক password এ set করেছেন?
  - [ ] `DB_NAME` সঠিক database name এ set করেছেন?
  - [ ] `DB_PORT=5432` - Render এ set করেছেন?

### For Static Files Issues:

- [ ] requirements.txt এ `whitenoise==6.7.0` আছে?
- [ ] settings.py এ `STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'` আছে?
- [ ] Build logs এ `Collecting static files` successful আছে?

---

## 🔧 Manual Fix Steps

যদি deployment fail থাকে, এই steps follow করুন:

### **Step 1: Clear and Re-Add All Variables**

```
1. Render Dashboard → Your Service → Settings
2. Environment section এ যান
3. সব পুরাতন variables delete করুন (Reset করুন)
4. নতুন করে সব add করুন (নিচের list থেকে)
```

**Minimum Required:**
```
DEBUG=False
RENDER=True
DJANGO_SETTINGS_MODULE=zonedelivery.settings
SECRET_KEY=<your-secure-key>
ALLOWED_HOSTS=zonedelivery.onrender.com
```

### **Step 2: Manual Deploy**

```
1. Dashboard → Your Service
2. Manual Deploy button খুঁজুন
3. "Deploy latest commit" ক্লিক করুন
4. Logs watch করুন
```

### **Step 3: Check Logs in Real-time**

```
Logs tab automatically refresh করে
কিছু minutes ধরে অপেক্ষা করুন deployment complete হওয়ার জন্য
```

---

## 📞 Critical Logs to Save

যদি still fail হয়, এই logs save করুন আমাকে পাঠানোর জন্য:

```
1. সম্পূর্ণ Build output (Build failed হলে)
2. সম্পূর্ণ Deploy output (Deploy failed হলে)
3. সব Environment Variables (passwords ছাড়া)
4. আপনার service name
5. আপনার GitHub repo link
```

---

## ✅ How to Check if Deploy is Working

### 1. **Check Service Status**
```
Dashboard → Service → Status
Should show: "Live" (green) না "Failed" (red)
```

### 2. **Check URL**
```
https://zonedelivery.onrender.com/
Should load করবে (500 error না দেখালে deployment successful)
```

### 3. **Check Admin Panel**
```
https://zonedelivery.onrender.com/admin/
Admin login page দেখাবে = Deploy successful ✓
```

---

## 🆘 Emergency Commands

যদি সবকিছু fail হয়ে যায়:

### **Restart Service**
```
Dashboard → Your Service → Settings
Scroll down → "Restart Service" ক্লিক করুন
```

### **Delete and Recreate**
```
Dashboard → Services → zonedelivery → Delete
তারপর নতুন করে Web Service create করুন
(এটি last resort - সব data lost হবে)
```

---

Last Updated: April 10, 2026
