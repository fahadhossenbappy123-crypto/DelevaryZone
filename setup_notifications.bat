@echo off
REM ZoneDelivery Notification System - Setup Script for Windows
REM Run this to apply all notification improvements

echo.
echo 🚀 ZoneDelivery Notification System Setup
echo ===========================================
echo.

REM Step 1: Create database migrations
echo 📊 Step 1: Creating database migrations...
python manage.py makemigrations
echo ✅ Migrations created
echo.

REM Step 2: Apply migrations
echo 📝 Step 2: Applying migrations to database...
python manage.py migrate
echo ✅ Database updated
echo.

REM Step 3: Note about Python shell
echo 🧪 Step 3: To test the notification system, run:
echo.
echo python manage.py shell
echo.
echo Then in the Python shell, run:
echo from django.contrib.auth.models import User
echo from shop.notification_service import create_notification
echo user = User.objects.first^(^)
echo create_notification^(user=user, notification_type='general', title='Test', message='Test message'^)
echo.

echo ✨ All done! Your notification system is ready.
echo.
echo 📍 Next steps:
echo 1. Run: python manage.py runserver
echo 2. Visit: http://localhost:8000/notifications/
echo 3. Visit: http://localhost:8000/notifications/preferences/
echo.
echo 📧 To enable email notifications, update settings.py with:
echo    - EMAIL_BACKEND
echo    - EMAIL_HOST
echo    - EMAIL_HOST_USER
echo    - EMAIL_HOST_PASSWORD
echo.
echo 📚 Read NOTIFICATION_SYSTEM_GUIDE.md for complete documentation
echo.
pause
