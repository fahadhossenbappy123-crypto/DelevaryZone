#!/bin/bash
# ZoneDelivery Notification System - Setup Script
# Run this to apply all notification improvements

echo "🚀 ZoneDelivery Notification System Setup"
echo "==========================================="
echo ""

# Step 1: Create database migrations
echo "📊 Step 1: Creating database migrations..."
python manage.py makemigrations
echo "✅ Migrations created"
echo ""

# Step 2: Apply migrations
echo "📝 Step 2: Applying migrations to database..."
python manage.py migrate
echo "✅ Database updated"
echo ""

# Step 3: Create a test notification (optional)
echo "🧪 Step 3: Testing notification system..."
python manage.py shell << EOF
from django.contrib.auth.models import User
from shop.notification_service import create_notification

# Find first user
user = User.objects.first()
if user:
    notif = create_notification(
        user=user,
        notification_type='general',
        title='Welcome to Notification System!',
        message='Your notification system is now ready. Visit /notifications/ to see your notifications.',
    )
    print(f"✅ Test notification created for {user.username}")
    print(f"   Visit: /notifications/ to see it")
else:
    print("⚠️  No users found. Create a user first.")
EOF
echo ""

echo "✨ All done! Your notification system is ready."
echo ""
echo "📍 Next steps:"
echo "1. Run: python manage.py runserver"
echo "2. Visit: http://localhost:8000/notifications/"
echo "3. Visit: http://localhost:8000/notifications/preferences/"
echo ""
echo "📧 To enable email notifications, update settings.py with:"
echo "   - EMAIL_BACKEND"
echo "   - EMAIL_HOST"
echo "   - EMAIL_HOST_USER"
echo "   - EMAIL_HOST_PASSWORD"
echo ""
echo "📚 Read NOTIFICATION_SYSTEM_GUIDE.md for complete documentation"
