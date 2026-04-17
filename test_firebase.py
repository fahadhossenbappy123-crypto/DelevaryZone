"""
Firebase Configuration Test Script
এটি চালান: python test_firebase.py
"""

import os
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Django setup
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zonedelivery.settings')
django.setup()

from shop.firebase_config import get_firebase_bucket, upload_to_firebase, delete_from_firebase
from io import BytesIO
from PIL import Image

def create_test_image():
    """একটি test image তৈরি করুন"""
    img = Image.new('RGB', (100, 100), color='red')
    img_io = BytesIO()
    img.save(img_io, 'JPEG')
    img_io.seek(0)
    img_io.name = 'test_image.jpg'
    img_io.content_type = 'image/jpeg'
    return img_io

def test_firebase_connection():
    """Firebase connection test করুন"""
    print("\n" + "="*50)
    print("🔥 FIREBASE CONNECTION TEST")
    print("="*50)
    
    try:
        bucket = get_firebase_bucket()
        if bucket:
            print(f"✅ Firebase Connected!")
            print(f"   Bucket Name: {bucket.name}")
            return True
        else:
            print("❌ Firebase bucket not available")
            return False
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return False

def test_file_upload():
    """Firebase এ file upload test করুন"""
    print("\n" + "="*50)
    print("📤 FILE UPLOAD TEST")
    print("="*50)
    
    try:
        test_image = create_test_image()
        firebase_url = upload_to_firebase(test_image, 'test/test_image.jpg')
        
        if firebase_url:
            print(f"✅ Upload Successful!")
            print(f"   URL: {firebase_url}")
            return firebase_url
        else:
            print("❌ Upload failed")
            return None
    except Exception as e:
        print(f"❌ Upload Error: {e}")
        return None

def test_file_deletion(firebase_url):
    """Firebase থেকে file delete test করুন"""
    if not firebase_url:
        print("\n⏭️ Skipping deletion test (no file to delete)")
        return
    
    print("\n" + "="*50)
    print("🗑️ FILE DELETION TEST")
    print("="*50)
    
    try:
        success = delete_from_firebase('test/test_image.jpg')
        if success:
            print("✅ Deletion Successful!")
        else:
            print("❌ Deletion failed")
    except Exception as e:
        print(f"❌ Deletion Error: {e}")

if __name__ == '__main__':
    print("\n🚀 Starting Firebase Tests...\n")
    
    # Test 1: Connection
    if test_firebase_connection():
        # Test 2: Upload
        firebase_url = test_file_upload()
        
        # Test 3: Delete
        test_file_deletion(firebase_url)
    
    print("\n" + "="*50)
    print("✨ All tests completed!")
    print("="*50 + "\n")
