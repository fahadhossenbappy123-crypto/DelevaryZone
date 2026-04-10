# Render Database Configuration - Step by Step

## Step 1: Go to Render Dashboard

1. Login to [render.com](https://render.com)
2. Select your Web Service: `zonedelivery`
3. Go to **Settings** → **Environment**

---

## Step 2: Add Environment Variables

### Option A: Using Render PostgreSQL (Recommended)

If Render auto-created a PostgreSQL database for you:

1. **Copy the DATABASE_URL** from Render PostgreSQL dashboard
2. Add it as environment variable:
   ```
   Key: DATABASE_URL
   Value: postgresql://user:password@host/database
   ```
3. Click "Save"
4. Render will auto-redeploy

---

### Option B: Using External PostgreSQL

If you have external database (like your current one):

Add these variables in Render Dashboard:

```
DB_ENGINE = django.db.backends.postgresql
DB_NAME = delevaryzone
DB_USER = delevaryzone_user
DB_PASSWORD = s1cbP1j6fXTrRvxKyssdRZywuLIww6a8
DB_HOST = dpg-d7c7hfjbc2fs73ep6ci0-a.oregon-postgres.render.com
DB_PORT = 5432
```

---

## Step 3: Verify Deployment

After adding environment variables:

1. Render will auto-redeploy
2. Check Deploy logs for errors
3. Try accessing admin: `https://your-app.onrender.com/admin/`
4. Login with:
   ```
   Username: adminbappy
   Password: bappy8800
   ```

---

## Troubleshooting

### Problem: "Connection refused"
→ Check DATABASE_URL is correct

### Problem: "Relation does not exist"
→ Migrations didn't run. Check build logs.

### Problem: Admin page won't load
→ Check if DEBUG = False causing issues. Set to True temporarily.

---

## Variables Summary

```
RENDER = True
DEBUG = False
DJANGO_SETTINGS_MODULE = zonedelivery.settings
ALLOWED_HOSTS = zonedelivery-1.onrender.com,localhost
DATABASE_URL = (your PostgreSQL connection string)
```

---

**That's it! Your app will work with all environment variables properly configured.** 🚀
