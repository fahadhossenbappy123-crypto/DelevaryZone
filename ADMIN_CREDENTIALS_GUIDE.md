# Admin User Configuration

## Where is Admin Credentials Stored?

### Code-based (Initial Setup)
```
File: shop/management/commands/create_admin_user.py
Lines: 13-15
```

**Current Credentials:**
```python
ADMIN_USERNAME = 'adminbappy'
ADMIN_EMAIL = 'admin@zonedelivery.com'
ADMIN_PASSWORD = 'bappy8800'
```

### How It Works

1. **Deployment Time**: When pushing to Render, `create_admin_user` command runs automatically
2. **Database**: Credentials are stored as hashed passwords in PostgreSQL
3. **Security**: Password is never stored plain in production - only in code for initialization

---

## How to Change Admin Credentials

### Step 1: Edit the Command File
Edit: `shop/management/commands/create_admin_user.py`

**Change these lines:**
```python
ADMIN_USERNAME = 'your_new_username'      # Line 13
ADMIN_EMAIL = 'your_email@example.com'    # Line 14
ADMIN_PASSWORD = 'your_new_password'      # Line 15
```

### Step 2: Push to GitHub
```bash
git add shop/management/commands/create_admin_user.py
git commit -m "Update admin credentials"
git push origin master
```

### Step 3: Redeploy on Render
- Go to Render Dashboard
- Click your service
- Click "Manual Deploy" or wait for auto-deploy
- The new admin user will be created

### Step 4: Verify
```
Login URL: https://your-app.onrender.com/admin/
Username: (your new username from Line 13)
Password: (your new password from Line 15)
```

---

## For Local Development

To create admin user locally:
```bash
python manage.py create_admin_user
```

This will use the same credentials from `create_admin_user.py`

---

## Security Notes

✅ Passwords are NOT stored in .env  
✅ Passwords are NOT in settings.py  
✅ Passwords are hashed in database  
✅ Only initial setup has hardcoded credentials  
✅ After creation, you can change password in Admin Panel  

---

## Alternative: Change Password in Admin Panel

After logging in:
1. Go to `https://your-app.onrender.com/admin/`
2. Click your username (top right)
3. Click "Change password"
4. Enter new password

This way you don't need to redeploy.
