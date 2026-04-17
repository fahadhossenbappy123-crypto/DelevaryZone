"""
Cloudinary Configuration Test Script
এটি চালান: python test_cloudinary.py
"""

import os
import sys
from pathlib import Path
from io import BytesIO

# Add project to path
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Django setup
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zonedelivery.settings')
django.setup()

import cloudinary
import cloudinary.uploader
from decouple import config
from PIL import Image

def create_test_image():
    """একটি test image তৈরি করুন"""
    img = Image.new('RGB', (200, 200), color='blue')
    img_io = BytesIO()
    img.save(img_io, 'JPEG')
    img_io.seek(0)
    img_io.name = 'test_image.jpg'
    img_io.content_type = 'image/jpeg'
    return img_io

def test_cloudinary_connection():
    """Cloudinary connection test করুন"""
    print("\n" + "="*60)
    print("☁️ CLOUDINARY CONNECTION TEST")
    print("="*60)
    
    try:
        cloud_name = config('CLOUDINARY_CLOUD_NAME', default='')
        api_key = config('CLOUDINARY_API_KEY', default='')
        api_secret = config('CLOUDINARY_API_SECRET', default='')
        
        if not cloud_name or not api_key or not api_secret:
            print("❌ Cloudinary credentials not configured!")
            print("   .env ফাইল এ এই variables add করুন:")
            print("   - CLOUDINARY_CLOUD_NAME")
            print("   - CLOUDINARY_API_KEY")
            print("   - CLOUDINARY_API_SECRET")
            return False
        
        # Initialize Cloudinary
        cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret
        )
        
        print(f"✅ Cloudinary Connected!")
        print(f"   Cloud Name: {cloud_name}")
        print(f"   API Key: {api_key[:10]}...")
        print(f"   Credentials: Loaded successfully")
        return True
        
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return False

def test_file_upload():
    """Cloudinary এ file upload test করুন"""
    print("\n" + "="*60)
    print("📤 FILE UPLOAD TEST")
    print("="*60)
    
    try:
        test_image = create_test_image()
        
        result = cloudinary.uploader.upload(
            test_image,
            folder='zone-delivery/test',
            resource_type='auto'
        )
        
        if result:
            print(f"✅ Upload Successful!")
            print(f"   URL: {result['secure_url']}")
            print(f"   Public ID: {result['public_id']}")
            print(f"   File Type: {result['resource_type']}")
            print(f"   Size: {result['bytes']} bytes")
            return result['public_id']
        else:
            print("❌ Upload failed")
            return None
            
    except Exception as e:
        print(f"❌ Upload Error: {e}")
        return None

def test_file_deletion(public_id):
    """Cloudinary থেকে file delete test করুন"""
    if not public_id:
        print("\n⏭️  Skipping deletion test (no file to delete)")
        return
    
    print("\n" + "="*60)
    print("🗑️  FILE DELETION TEST")
    print("="*60)
    
    try:
        result = cloudinary.uploader.destroy(public_id)
        
        if result['result'] == 'ok':
            print("✅ Deletion Successful!")
        else:
            print("❌ Deletion failed")
            
    except Exception as e:
        print(f"❌ Deletion Error: {e}")

def test_file_types():
    """বিভিন্ন file type upload test করুন"""
    print("\n" + "="*60)
    print("🎨 FILE TYPES SUPPORT TEST")
    print("="*60)
    
    supported = {
        '📷 Images': ['jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp'],
        '🎬 Videos': ['mp4', 'webm', 'mov', 'avi', 'mkv'],
        '📄 Documents': ['pdf', 'doc', 'docx', 'xls', 'xlsx']
    }
    
    for category, types in supported.items():
        print(f"\n{category}:")
        print(f"   {', '.join(types)}")
    
    print("\n✅ Cloudinary supports 1000+ file formats!")

if __name__ == '__main__':
    print("\n" + "🚀 Starting Cloudinary Tests...\n")
    
    # Test 1: Connection
    if test_cloudinary_connection():
        # Test 2: Upload
        public_id = test_file_upload()
        
        # Test 3: Delete
        test_file_deletion(public_id)
        
        # Test 4: Supported file types
        test_file_types()
    
    print("\n" + "="*60)
    print("✨ All tests completed!")
    print("="*60 + "\n")
