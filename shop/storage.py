"""
Custom Cloudinary Storage Backend for Django
Hybrid backend that handles both old local paths and new Cloudinary uploads
"""

from django.core.files.storage import Storage, FileSystemStorage
from django.core.files.base import ContentFile
import cloudinary
import cloudinary.uploader
import cloudinary.api
import os
from io import BytesIO

class CloudinaryStorage(Storage):
    """
    Cloudinary storage backend যা সরাসরি cloudinary.uploader ব্যবহার করে
    নতুন uploads Cloudinary এ যায়
    """
    
    def _save(self, name, content):
        """
        File কে Cloudinary তে save করুন
        """
        try:
            # File পড়ুন
            if hasattr(content, 'read'):
                file_data = content.read()
            else:
                file_data = content
            
            # Cloudinary এ upload করুন
            result = cloudinary.uploader.upload(
                file_data,
                resource_type='auto',  # Auto detect image/video
                folder='zone-delivery'
            )
            
            # Cloudinary public_id return করুন
            return result['public_id']
            
        except Exception as e:
            print(f"Cloudinary upload error: {e}")
            raise
    
    def _open(self, name, mode='rb'):
        """
        Cloudinary থেকে file পড়ুন
        """
        try:
            bucket = cloudinary.api.resource(name)
            if bucket:
                return ContentFile(bucket.get('url'))
        except:
            pass
        return None
    
    def delete(self, name):
        """
        Cloudinary থেকে file delete করুন
        """
        try:
            cloudinary.uploader.destroy(name)
        except Exception as e:
            print(f"Cloudinary delete error: {e}")
    
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
        List directory (not implemented for Cloudinary)
        """
        raise NotImplementedError('Cloudinary does not support directory listing')
    
    def size(self, name):
        """
        Get file size
        """
        try:
            resource = cloudinary.api.resource(name)
            return resource.get('bytes', 0)
        except:
            return 0
    
    def url(self, name):
        """
        Get file URL - supports both Cloudinary and local paths for backward compatibility
        
        Returns:
            Secure Cloudinary URL or local media URL
        """
        cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME', '')
        
        # যদি পুরাতন local path হয় (e.g., /media/products/...
) তাহলে local URL return করুন
        if '/' in name and not name.startswith('zone-delivery'):
            # Old local storage path
            return f'/media/{name}'
        
        # নতুন Cloudinary public_id এর জন্য Cloudinary URL
        if not cloud_name:
            return f'/media/{name}'
        
        # Format: https://res.cloudinary.com/{cloud}/image/upload/{public_id}
        return f'https://res.cloudinary.com/{cloud_name}/image/upload/{name}'
    
    def get_accessed_time(self, name):
        """
        Cloudinary দ্বারা সমর্থিত নয়
        """
        raise NotImplementedError('Cloudinary does not support accessed time')
    
    def get_created_time(self, name):
        """
        Cloudinary দ্বারা সমর্থিত নয়
        """
        raise NotImplementedError('Cloudinary does not support created time')
    
    def get_modified_time(self, name):
        """
        Cloudinary দ্বারা সমর্থিত নয়
        """
        raise NotImplementedError('Cloudinary does not support modified time')
