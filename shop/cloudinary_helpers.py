"""
Cloudinary Helper Functions - Django views এ ব্যবহার করুন
"""

import cloudinary
import cloudinary.uploader
from django.conf import settings

def upload_image(file, folder='products'):
    """
    Cloudinary এ image upload করুন
    
    Usage:
        from shop.cloudinary_helpers import upload_image
        url = upload_image(request.FILES['image'], 'products')
    
    Args:
        file: Django UploadedFile
        folder: Cloudinary folder name
    
    Returns:
        {'url': secure_url, 'public_id': public_id} or None
    """
    try:
        result = cloudinary.uploader.upload(
            file,
            folder=f'zone-delivery/{folder}',
            resource_type='auto',
            quality='auto',  # Auto optimize quality
            fetch_format='auto'  # Auto format conversion
        )
        
        return {
            'url': result['secure_url'],
            'public_id': result['public_id'],
            'width': result.get('width'),
            'height': result.get('height')
        }
    except Exception as e:
        print(f"Upload error: {e}")
        return None


def delete_image(public_id):
    """
    Cloudinary থেকে image delete করুন
    
    Usage:
        from shop.cloudinary_helpers import delete_image
        delete_image(product.image.public_id)
    
    Args:
        public_id: Cloudinary public_id
    
    Returns:
        True/False
    """
    try:
        result = cloudinary.uploader.destroy(public_id)
        return result['result'] == 'ok'
    except Exception as e:
        print(f"Delete error: {e}")
        return False


def get_optimized_url(public_id, width=None, height=None):
    """
    Optimized image URL generate করুন (different sizes)
    
    Usage:
        from shop.cloudinary_helpers import get_optimized_url
        thumbnail = get_optimized_url(public_id, width=200, height=200)
    
    Args:
        public_id: Cloudinary public_id
        width: Width in pixels (optional)
        height: Height in pixels (optional)
    
    Returns:
        Optimized URL string
    """
    url = f"https://res.cloudinary.com/{settings.CLOUDINARY['cloud_name']}/image/upload/"
    
    if width or height:
        if width and height:
            url += f"w_{width},h_{height},c_fill/"
        elif width:
            url += f"w_{width},c_scale/"
        elif height:
            url += f"h_{height},c_scale/"
    
    url += public_id
    return url


def get_thumbnail_url(public_id, size=200):
    """
    Thumbnail URL generate করুন
    
    Usage:
        from shop.cloudinary_helpers import get_thumbnail_url
        thumb = get_thumbnail_url(public_id)
    
    Args:
        public_id: Cloudinary public_id
        size: Thumbnail size (default 200x200)
    
    Returns:
        Thumbnail URL
    """
    return get_optimized_url(public_id, width=size, height=size)


def upload_video(file, folder='videos'):
    """
    Cloudinary এ video upload করুন
    
    Usage:
        from shop.cloudinary_helpers import upload_video
        video_url = upload_video(request.FILES['video'], 'products')
    
    Args:
        file: Django UploadedFile (video)
        folder: Cloudinary folder name
    
    Returns:
        {'url': secure_url, 'public_id': public_id} or None
    """
    try:
        result = cloudinary.uploader.upload(
            file,
            folder=f'zone-delivery/{folder}',
            resource_type='video',
            eager=[
                {
                    'width': 300,
                    'height': 300,
                    'crop': 'pad',
                    'background': 'auto',
                    'format': 'jpg'
                }
            ]
        )
        
        return {
            'url': result['secure_url'],
            'public_id': result['public_id'],
            'duration': result.get('duration'),
            'format': result.get('format')
        }
    except Exception as e:
        print(f"Video upload error: {e}")
        return None
