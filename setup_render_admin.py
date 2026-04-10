#!/usr/bin/env python
"""
Script to create admin user in Render PostgreSQL database
Run: python setup_render_admin.py
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zonedelivery.settings')

# Set Render environment
os.environ['RENDER'] = 'True'
os.environ['DB_ENGINE'] = 'django.db.backends.postgresql'
os.environ['DB_NAME'] = 'delevaryzone'
os.environ['DB_USER'] = 'delevaryzone_user'
os.environ['DB_PASSWORD'] = 's1cbP1j6fXTrRvxKyssdRZywuLIww6a8'
os.environ['DB_HOST'] = 'dpg-d7c7hfjbc2fs73ep6ci0-a.oregon-postgres.render.com'
os.environ['DB_PORT'] = '5432'

django.setup()

from django.contrib.auth.models import User

# Admin credentials
ADMIN_USERNAME = 'adminbappy'
ADMIN_EMAIL = 'admin@zonedelivery.com'
ADMIN_PASSWORD = 'bappy8800'

print("=" * 60)
print("RENDER ADMIN USER SETUP")
print("=" * 60)

try:
    # Check if already exists
    existing = User.objects.filter(username=ADMIN_USERNAME).exists()
    
    if existing:
        print(f"\nAdmin user '{ADMIN_USERNAME}' already exists!")
        
        # Show info
        admin = User.objects.get(username=ADMIN_USERNAME)
        print(f"  Email: {admin.email}")
        print(f"  Last login: {admin.last_login}")
        
    else:
        # Create new admin
        admin = User.objects.create_superuser(
            username=ADMIN_USERNAME,
            email=ADMIN_EMAIL,
            password=ADMIN_PASSWORD
        )
        
        print(f"\nSuccessfully created admin user!")
        print(f"  Username: {admin.username}")
        print(f"  Email: {admin.email}")
        print(f"  Password: {ADMIN_PASSWORD}")
        
    print("\n" + "=" * 60)
    print("NEXT STEPS:")
    print("=" * 60)
    print(f"1. Go to Render Admin: https://your-app.onrender.com/admin/")
    print(f"2. Login with:")
    print(f"   Username: {ADMIN_USERNAME}")
    print(f"   Password: {ADMIN_PASSWORD}")
    print("=" * 60)
    
except Exception as e:
    print(f"\nError: {str(e)}")
    print("\nTroubleshooting:")
    print("1. Check database credentials in this file")
    print("2. Make sure PostgreSQL database is accessible")
    print("3. Run migrations first: python manage.py migrate")
    sys.exit(1)
