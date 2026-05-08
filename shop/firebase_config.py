import firebase_admin
from firebase_admin import credentials, storage, db
import json
import os
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

# Firebase configuration
FIREBASE_CREDENTIALS = str(BASE_DIR / config('FIREBASE_CREDENTIALS', default='zone-delevary-firebase-adminsdk-fbsvc-b0b84509c0.json'))
FIREBASE_DATABASE_URL = config('FIREBASE_DATABASE_URL', default='')


def _guess_database_url():
    if FIREBASE_DATABASE_URL:
        return FIREBASE_DATABASE_URL

    try:
        with open(FIREBASE_CREDENTIALS, 'r', encoding='utf-8') as f:
            data = json.load(f)
        project_id = data.get('project_id')
        if project_id:
            return f'https://{project_id}.firebaseio.com'
    except Exception:
        pass

    return None

FIREBASE_DATABASE_URL = _guess_database_url()

# Initialize Firebase (শুধু একবার initialize করুন)
try:
    firebase_admin.get_app()
except ValueError:
    try:
        creds = credentials.Certificate(FIREBASE_CREDENTIALS)
        options = {
            'storageBucket': 'zone-delevary.appspot.com'
        }
        if FIREBASE_DATABASE_URL:
            options['databaseURL'] = FIREBASE_DATABASE_URL

        firebase_admin.initialize_app(creds, options)
        print("✅ Firebase initialized successfully!")
        if FIREBASE_DATABASE_URL:
            print(f"   Realtime DB: {FIREBASE_DATABASE_URL}")
    except Exception as e:
        print(f"❌ Firebase initialization error: {e}")


def get_firebase_bucket():
    """Firebase storage bucket return করুন"""
    try:
        return storage.bucket()
    except Exception as e:
        print(f"Error getting Firebase bucket: {e}")
        return None


def get_firebase_db_ref(path=None):
    """Firebase Realtime Database reference return করুন"""
    if not FIREBASE_DATABASE_URL:
        print("Firebase Realtime Database URL not configured.")
        return None

    try:
        return db.reference(path or '/')
    except Exception as e:
        print(f"Error getting Firebase DB reference: {e}")
        return None


def push_realtime_notification(notification):
    """একটি notification কে Firebase Realtime DB এ push করুন"""
    try:
        ref = get_firebase_db_ref(f'notifications/{notification.user_id}/{notification.id}')
        if not ref:
            return False

        data = {
            'id': notification.id,
            'user_id': notification.user_id,
            'type': notification.notification_type,
            'title': notification.title,
            'message': notification.message,
            'order_id': notification.order.order_id if notification.order else None,
            'is_read': notification.is_read,
            'is_deleted': notification.is_deleted,
            'read_at': notification.read_at.isoformat() if notification.read_at else None,
            'created_at': notification.created_at.isoformat() if notification.created_at else None,
        }
        ref.set(data)
        return True
    except Exception as e:
        print(f"Firebase push notification error: {e}")
        return False


def update_realtime_notification_status(notification):
    """Read / status update sync করুন Firebase Realtime DB এ"""
    try:
        ref = get_firebase_db_ref(f'notifications/{notification.user_id}/{notification.id}')
        if not ref:
            return False

        ref.update({
            'is_read': notification.is_read,
            'read_at': notification.read_at.isoformat() if notification.read_at else None,
            'is_deleted': notification.is_deleted,
        })
        return True
    except Exception as e:
        print(f"Firebase update notification status error: {e}")
        return False


def set_user_location(user_id, latitude, longitude, is_in_service, zones=None):
    """ব্যবহারকারীর location data Firebase Realtime DB এ আপডেট করুন"""
    try:
        if not user_id:
            return False

        ref = get_firebase_db_ref(f'locations/{user_id}')
        if not ref:
            return False

        data = {
            'latitude': latitude,
            'longitude': longitude,
            'is_in_service': is_in_service,
            'zones': zones or [],
            'last_checked': db.SERVER_TIMESTAMP,
        }
        ref.set(data)
        return True
    except Exception as e:
        print(f"Firebase set user location error: {e}")
        return False


def push_notification_preferences(user):
    """User notification preferences Firebase Realtime DB এ sync করুন"""
    try:
        if not user or not hasattr(user, 'notification_preference'):
            return False

        prefs = user.notification_preference
        ref = get_firebase_db_ref(f'user_preferences/{user.id}')
        if not ref:
            return False

        ref.set({
            'order_updates': prefs.order_updates,
            'order_confirmation': prefs.order_confirmation,
            'rider_assignments': prefs.rider_assignments,
            'general_notifications': prefs.general_notifications,
            'email_on_order_updates': prefs.email_on_order_updates,
            'email_on_delivery': prefs.email_on_delivery,
            'email_on_cancellation': prefs.email_on_cancellation,
            'email_digests': prefs.email_digests,
            'enable_sound': prefs.enable_sound,
            'enable_browser_notifications': prefs.enable_browser_notifications,
            'quiet_hours_enabled': prefs.quiet_hours_enabled,
            'quiet_hours_start': prefs.quiet_hours_start.isoformat() if prefs.quiet_hours_start else None,
            'quiet_hours_end': prefs.quiet_hours_end.isoformat() if prefs.quiet_hours_end else None,
            'updated_at': prefs.updated_at.isoformat() if prefs.updated_at else None,
        })
        return True
    except Exception as e:
        print(f"Firebase push notification preferences error: {e}")
        return False


def upload_to_firebase(file, destination_path):
    """
    Firebase এ file upload করুন
    
    Args:
        file: Django UploadedFile object
        destination_path: Firebase এ file path (e.g., 'products/image.jpg')
    
    Returns:
        Public URL অথবা None (error হলে)
    """
    try:
        bucket = get_firebase_bucket()
        if not bucket:
            return None
        
        blob = bucket.blob(destination_path)
        blob.upload_from_string(
            file.read(),
            content_type=file.content_type
        )
        
        # Public URL তৈরি করুন
        file.seek(0)  # Reset file pointer
        return f"https://firebasestorage.googleapis.com/v0/b/{bucket.name}/o/{destination_path}?alt=media"
    
    except Exception as e:
        print(f"Firebase upload error: {e}")
        return None


def delete_from_firebase(destination_path):
    """Firebase থেকে file delete করুন"""
    try:
        bucket = get_firebase_bucket()
        if bucket:
            blob = bucket.blob(destination_path)
            blob.delete()
            return True
    except Exception as e:
        print(f"Firebase delete error: {e}")
    
    return False
