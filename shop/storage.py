"""
Cloudinary Storage Backend for Django
Pure Cloudinary storage - No local fallback
All uploads go directly to Cloudinary cloud
"""

from django.core.files.storage import Storage
from django.core.files.base import ContentFile
import cloudinary
import cloudinary.uploader
import cloudinary.api
import logging
from decouple import config as decouple_config

logger = logging.getLogger(__name__)

class CloudinaryStorage(Storage):
    """
    Pure Cloudinary storage backend
    - ALL files go to Cloudinary
    - NO local storage fallback
    - Persistent across server restarts
    """
    
    def __init__(self):
        """Initialize and verify Cloudinary config"""
        cloud_name = decouple_config('CLOUDINARY_CLOUD_NAME', default='')
        api_key = decouple_config('CLOUDINARY_API_KEY', default='')
        api_secret = decouple_config('CLOUDINARY_API_SECRET', default='')
        
        if not all([cloud_name, api_key, api_secret]):
            logger.error("❌ Cloudinary credentials missing! Set environment variables in .env")
        
        # Configure cloudinary
        cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret,
            secure=True
        )
    
    def _save(self, name, content):
        """
        Save file directly to Cloudinary
        
        Args:
            name: Filename (e.g., 'products/image.jpg')
            content: File content
        
        Returns:
            Cloudinary public_id (stored in database)
        """
        try:
            # Determine folder from name
            if 'products' in name:
                folder = 'zone-delivery/products'
            elif 'category' in name:
                folder = 'zone-delivery/categories'
            elif 'profile' in name or 'avatar' in name:
                folder = 'zone-delivery/profile_pics'
            else:
                folder = 'zone-delivery/media'
            
            # Read file content
            if hasattr(content, 'read'):
                file_data = content.read()
                if hasattr(content, 'seek'):
                    content.seek(0)
            else:
                file_data = content
            
            # Upload to Cloudinary
            logger.info(f"📤 Uploading to Cloudinary: {name} → {folder}")
            
            result = cloudinary.uploader.upload(
                file_data,
                folder=folder,
                resource_type='auto',  # Image, video, or raw
                overwrite=False,  # Prevent overwriting
                unique_filename=True,  # Generate unique names
                quality='auto',  # Auto quality optimization
                fetch_format='auto'  # Auto format conversion
            )
            
            public_id = result['public_id']
            logger.info(f"✅ Upload successful: {public_id}")
            
            return public_id
            
        except Exception as e:
            logger.error(f"❌ Cloudinary upload failed: {str(e)}")
            raise
    
    def _open(self, name, mode='rb'):
        """
        Open file from Cloudinary
        """
        try:
            resource = cloudinary.api.resource(name)
            if resource and resource.get('secure_url'):
                return ContentFile(resource['secure_url'].encode())
        except Exception as e:
            logger.error(f"Error opening file from Cloudinary: {e}")
        return None
    
    def delete(self, name):
        """
        Delete file from Cloudinary
        """
        try:
            logger.info(f"🗑️  Deleting from Cloudinary: {name}")
            cloudinary.uploader.destroy(name)
            logger.info(f"✅ Deleted: {name}")
        except Exception as e:
            logger.error(f"Error deleting from Cloudinary: {e}")
    
    def exists(self, name):
        """
        Check if file exists in Cloudinary
        """
        try:
            cloudinary.api.resource(name)
            return True
        except:
            return False
    
    def listdir(self, path):
        """
        Cloudinary does not support directory listing
        """
        raise NotImplementedError('Cloudinary does not support directory listing')
    
    def size(self, name):
        """
        Get file size from Cloudinary
        """
        try:
            resource = cloudinary.api.resource(name)
            return resource.get('bytes', 0)
        except:
            return 0
    
    def url(self, name):
        """
        Generate Cloudinary secure URL
        ONLY returns Cloudinary URLs - NO local fallback
        
        Returns:
            Secure Cloudinary URL
        """
        cloud_name = decouple_config('CLOUDINARY_CLOUD_NAME', default='')
        
        if not cloud_name:
            logger.error("❌ CLOUDINARY_CLOUD_NAME not set!")
            return ''
        
        # Generate Cloudinary URL
        url = f'https://res.cloudinary.com/{cloud_name}/image/upload/{name}'
        return url
    
    def get_accessed_time(self, name):
        raise NotImplementedError('Cloudinary does not support accessed time')
    
    def get_created_time(self, name):
        raise NotImplementedError('Cloudinary does not support created time')
    
    def get_modified_time(self, name):
        raise NotImplementedError('Cloudinary does not support modified time')
