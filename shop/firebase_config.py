import firebase_admin
from firebase_admin import credentials, storage
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Firebase credentials JSON file path - root directory থেকে
FIREBASE_CREDENTIALS = str(BASE_DIR / 'zone-delevary-firebase-adminsdk-fbsvc-b0b84509c0.json')

# Initialize Firebase (শুধু একবার initialize করুন)
try:
    # Check if default app already exists
    firebase_admin.get_app()
except ValueError:
    # App doesn't exist, initialize it
    try:
        creds = credentials.Certificate(FIREBASE_CREDENTIALS)
        firebase_admin.initialize_app(creds, {
            'storageBucket': 'zone-delevary.appspot.com'
        })
        print("✅ Firebase initialized successfully!")
    except Exception as e:
        print(f"❌ Firebase initialization error: {e}")

def get_firebase_bucket():
    """Firebase storage bucket return করুন"""
    try:
        return storage.bucket()
    except Exception as e:
        print(f"Error getting Firebase bucket: {e}")
        return None


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
