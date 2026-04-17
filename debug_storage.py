import sys
import traceback

# Test 1: Import CloudinaryStorage directly
print("="*70)
print("TEST 1: Import CloudinaryStorage")
print("="*70)
try:
    from shop.storage import CloudinaryStorage
    print("✅ CloudinaryStorage imported")
except Exception as e:
    print(f"❌ Import failed: {e}")
    traceback.print_exc()
    sys.exit(1)

# Test 2: Instantiate CloudinaryStorage
print("\n" + "="*70)
print("TEST 2: Instantiate CloudinaryStorage")
print("="*70)
try:
    cs = CloudinaryStorage()
    print("✅ CloudinaryStorage instantiated")
    print(f"   Class: {cs.__class__.__name__}")
except Exception as e:
    print(f"❌ Instantiation failed: {e}")
    traceback.print_exc()
    sys.exit(1)

# Test 3: Load via Django
print("\n" + "="*70)
print("TEST 3: Load via Django default_storage")
print("="*70)
try:
    import django
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zonedelivery.settings')
    django.setup()
    
    from django.core.files.storage import default_storage
    print(f"✅ Default storage loaded")
    print(f"   Class: {default_storage.__class__.__name__}")
    print(f"   Module: {default_storage.__class__.__module__}")
    
    if 'CloudinaryStorage' not in str(default_storage.__class__):
        print("⚠️  WARNING: CloudinaryStorage not active!")
        print("   Check if there are initialization errors")
        
except Exception as e:
    print(f"❌ Django loading failed: {e}")
    traceback.print_exc()
    sys.exit(1)

print("\n✅ All debug tests completed")
