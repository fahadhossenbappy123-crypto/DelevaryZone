"""
Cloudinary Upload Test & Verification
Tests the pure Cloudinary storage setup
"""

import os
import sys
import django
from io import BytesIO
from pathlib import Path

# Setup Django
sys.path.insert(0, str(Path(__file__).resolve().parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zonedelivery.settings')
django.setup()

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from shop.models import Product, Category
from PIL import Image
import cloudinary

def create_test_image():
    """Create a test image"""
    img = Image.new('RGB', (400, 400), color='green')
    img_io = BytesIO()
    img.save(img_io, 'JPEG')
    img_io.seek(0)
    img_io.name = 'test_product_image.jpg'
    img_io.content_type = 'image/jpeg'
    return img_io

def test_cloudinary_config():
    """Test Cloudinary configuration"""
    print("\n" + "="*70)
    print("🔧 CLOUDINARY CONFIGURATION TEST")
    print("="*70)
    
    from decouple import config
    
    cloud_name = config('CLOUDINARY_CLOUD_NAME', default='')
    api_key = config('CLOUDINARY_API_KEY', default='')
    api_secret = config('CLOUDINARY_API_SECRET', default='')
    
    print(f"Cloud Name: {cloud_name if cloud_name else '❌ NOT SET'}")
    print(f"API Key: {'✅' if api_key else '❌ NOT SET'}")
    print(f"API Secret: {'✅' if api_secret else '❌ NOT SET'}")
    
    if not all([cloud_name, api_key, api_secret]):
        print("\n❌ Cloudinary credentials not configured!")
        return False
    
    print("\n✅ Cloudinary credentials configured")
    return True

def test_storage_backend():
    """Test storage backend"""
    print("\n" + "="*70)
    print("📦 STORAGE BACKEND TEST")
    print("="*70)
    
    print(f"Default Storage: {default_storage.__class__.__name__}")
    print(f"Storage Path: {default_storage.__class__.__module__}.{default_storage.__class__.__name__}")
    
    if 'CloudinaryStorage' in str(default_storage.__class__):
        print("✅ CloudinaryStorage is active")
        return True
    else:
        print("❌ CloudinaryStorage not active!")
        return False

def test_direct_upload():
    """Test direct file upload"""
    print("\n" + "="*70)
    print("📤 DIRECT UPLOAD TEST")
    print("="*70)
    
    try:
        test_image = create_test_image()
        
        print(f"Uploading test image...")
        
        # Use default_storage to upload
        filename = default_storage.save('test/test_image.jpg', test_image)
        
        print(f"✅ Upload successful!")
        print(f"   Filename: {filename}")
        
        # Get URL
        url = default_storage.url(filename)
        print(f"   URL: {url}")
        
        # Check if file exists
        exists = default_storage.exists(filename)
        print(f"   File exists: {'✅ Yes' if exists else '❌ No'}")
        
        # Clean up
        default_storage.delete(filename)
        print(f"   Cleanup: ✅ Deleted")
        
        return True
        
    except Exception as e:
        print(f"❌ Upload failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_cloudinary_api():
    """Test Cloudinary API directly"""
    print("\n" + "="*70)
    print("☁️ CLOUDINARY API TEST")
    print("="*70)
    
    try:
        import cloudinary.uploader
        
        print(f"Testing Cloudinary API...")
        
        # Create test file
        test_image = create_test_image()
        
        # Upload
        result = cloudinary.uploader.upload(
            test_image,
            folder='zone-delivery/test',
            resource_type='auto'
        )
        
        print(f"✅ Cloudinary API working!")
        print(f"   Public ID: {result['public_id']}")
        print(f"   URL: {result['secure_url']}")
        print(f"   Format: {result['format']}")
        print(f"   Size: {result['bytes']} bytes")
        
        # Delete test file
        cloudinary.uploader.destroy(result['public_id'])
        print(f"   Cleanup: ✅ Deleted from Cloudinary")
        
        return True
        
    except Exception as e:
        print(f"❌ Cloudinary API test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_model_save():
    """Test saving via Django model"""
    print("\n" + "="*70)
    print("🗂️ DJANGO MODEL SAVE TEST")
    print("="*70)
    
    try:
        # Create test category first
        category, _ = Category.objects.get_or_create(
            name='Test Category',
            defaults={'slug': 'test-category'}
        )
        
        test_image = create_test_image()
        
        print(f"Creating product with image...")
        
        product = Product(
            title='Test Product',
            description='Test product description',
            price=100.00,
            category=category,
            stock=10,
            image=ContentFile(test_image.getvalue(), name='test.jpg')
        )
        product.save()
        
        print(f"✅ Product saved!")
        print(f"   Product ID: {product.id}")
        print(f"   Image field: {product.image.name}")
        print(f"   Image URL: {product.image.url}")
        
        # Verify in database
        retrieved = Product.objects.get(id=product.id)
        print(f"   Retrieved from DB: ✅")
        print(f"   Stored image path: {retrieved.image.name}")
        
        # Clean up
        product.delete()
        print(f"   Cleanup: ✅ Product deleted")
        
        return True
        
    except Exception as e:
        print(f"❌ Model save test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("\n" + "🚀 CLOUDINARY UPLOAD SYSTEM TEST" + "\n")
    
    results = {
        'Config': test_cloudinary_config(),
        'Storage Backend': test_storage_backend(),
        'Cloudinary API': test_cloudinary_api(),
        'Direct Upload': test_direct_upload(),
        'Django Model': test_model_save(),
    }
    
    print("\n" + "="*70)
    print("📊 TEST RESULTS")
    print("="*70)
    
    for test, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test}: {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*70)
    if all_passed:
        print("✅ ALL TESTS PASSED - CLOUDINARY UPLOAD SYSTEM WORKING!")
        print("="*70)
        return 0
    else:
        print("❌ SOME TESTS FAILED - CHECK CONFIGURATION")
        print("="*70)
        return 1

if __name__ == '__main__':
    sys.exit(main())
