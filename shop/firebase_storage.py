from django.core.files.storage import Storage
from django.core.files.base import ContentFile
import os
import uuid
from .firebase_config import upload_to_firebase, delete_from_firebase, get_firebase_bucket

class FirebaseStorage(Storage):
    """Django এর জন্য Firebase Storage backend"""
    
    def __init__(self, location=''):
        self.location = location
    
    def _open(self, name, mode='rb'):
        """Firebase থেকে file open করুন"""
        bucket = get_firebase_bucket()
        if not bucket:
            raise IOError(f"Cannot open '{name}' without Firebase bucket")
        
        blob = bucket.blob(f"{self.location}/{name}")
        return ContentFile(blob.download_as_bytes())
    
    def _save(self, name, content):
        """Firebase এ file save করুন"""
        # Unique filename তৈরি করুন
        if not name:
            ext = getattr(content, 'name', '').split('.')[-1] or 'file'
            name = f"{uuid.uuid4()}.{ext}"
        
        path = f"{self.location}/{name}" if self.location else name
        
        # Upload করুন
        url = upload_to_firebase(content, path)
        if url:
            return name
        
        raise IOError(f"Failed to upload '{name}' to Firebase")
    
    def delete(self, name):
        """Firebase থেকে file delete করুন"""
        path = f"{self.location}/{name}" if self.location else name
        delete_from_firebase(path)
    
    def exists(self, name):
        """Check করুন file exist করে কিনা"""
        try:
            bucket = get_firebase_bucket()
            if bucket:
                path = f"{self.location}/{name}" if self.location else name
                blob = bucket.blob(path)
                return blob.exists()
        except:
            pass
        return False
    
    def url(self, name):
        """Firebase এ file এর public URL return করুন"""
        bucket = get_firebase_bucket()
        if bucket:
            path = f"{self.location}/{name}" if self.location else name
            return f"https://firebasestorage.googleapis.com/v0/b/{bucket.name}/o/{path}?alt=media"
        return name
    
    def get_accessed_time(self, name):
        """Last accessed time (Firebase এ available নয়)"""
        raise NotImplementedError
    
    def get_created_time(self, name):
        """Created time (Firebase এ available নয়)"""
        raise NotImplementedError
    
    def get_modified_time(self, name):
        """Modified time (Firebase এ available নয়)"""
        raise NotImplementedError
    
    def listdir(self, path):
        """Firebase folder এর contents list করুন"""
        raise NotImplementedError
    
    def size(self, name):
        """File size return করুন"""
        try:
            bucket = get_firebase_bucket()
            if bucket:
                path = f"{self.location}/{name}" if self.location else name
                blob = bucket.blob(path)
                blob.reload()
                return blob.size
        except:
            pass
        return 0
