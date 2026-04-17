"""
Cloudinary Configuration Module

কীভাবে setup করতে হবে:
1. https://cloudinary.com/users/register/free এ signup করুন
2. Dashboard এ যান (https://cloudinary.com/console/c_a52411ee76c6c8217a92299801b)
3. আপনার credentials দেখবেন:
   - Cloud Name
   - API Key
   - API Secret

4. .env ফাইল এ এই variables যোগ করুন:
   CLOUDINARY_CLOUD_NAME=your-cloud-name
   CLOUDINARY_API_KEY=your-api-key
   CLOUDINARY_API_SECRET=your-api-secret
"""

import cloudinary
import cloudinary.api
import cloudinary.uploader
from decouple import config

# Cloudinary Setup
CLOUDINARY_CLOUD_NAME = config('CLOUDINARY_CLOUD_NAME', default='')
CLOUDINARY_API_KEY = config('CLOUDINARY_API_KEY', default='')
CLOUDINARY_API_SECRET = config('CLOUDINARY_API_SECRET', default='')

# Cloudinary Initialize করুন
cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET
)


def upload_to_cloudinary(file, folder='zone-delivery'):
    """
    Cloudinary এ file upload করুন
    
    Args:
        file: Django UploadedFile object
        folder: Cloudinary এ folder name (e.g., 'products', 'profile_pics')
    
    Returns:
        dict with 'secure_url' বা None (error হলে)
    """
    try:
        result = cloudinary.uploader.upload(
            file,
            folder=folder,
            resource_type='auto',  # auto-detect করবে image/video
            timeout=60
        )
        return result
    except Exception as e:
        print(f"❌ Cloudinary upload error: {e}")
        return None


def delete_from_cloudinary(public_id):
    """
    Cloudinary থেকে file delete করুন
    
    Args:
        public_id: Cloudinary এ file এর public_id
    
    Returns:
        True/False
    """
    try:
        cloudinary.uploader.destroy(public_id)
        return True
    except Exception as e:
        print(f"❌ Cloudinary delete error: {e}")
        return False


def get_cloudinary_url(public_id):
    """
    Cloudinary URL generate করুন
    
    Args:
        public_id: Cloudinary এ file এর public_id
    
    Returns:
        Secure URL string
    """
    return f"https://res.cloudinary.com/{CLOUDINARY_CLOUD_NAME}/image/upload/{public_id}"
