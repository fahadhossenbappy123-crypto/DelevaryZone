"""
Django management command to migrate old local images to Cloudinary

Usage:
    python manage.py migrate_images_to_cloudinary
"""

from django.core.management.base import BaseCommand
from django.conf import settings
from shop.models import Product, Category, UserProfile
import cloudinary
import cloudinary.uploader
import os

class Command(BaseCommand):
    help = 'Migrate old local images to Cloudinary'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be migrated without actually doing it',
        )
        
        parser.add_argument(
            '--model',
            type=str,
            default='all',
            help='Specific model: Product, Category, UserProfile, or all',
        )
    
    def handle(self, *args, **options):
        dry_run = options.get('dry_run', False)
        model_name = options.get('model', 'all').lower()
        
        self.stdout.write("🔄 Starting image migration to Cloudinary...\n")
        
        if dry_run:
            self.stdout.write(self.style.WARNING("⚠️  DRY RUN MODE - No changes will be made\n"))
        
        # Migrate models
        if model_name in ['all', 'product']:
            self.migrate_products(dry_run)
        
        if model_name in ['all', 'category']:
            self.migrate_categories(dry_run)
        
        if model_name in ['all', 'userprofile']:
            self.migrate_userprofiles(dry_run)
        
        self.stdout.write(self.style.SUCCESS("\n✅ Migration completed!"))
    
    def migrate_products(self, dry_run=False):
        """Migrate Product images to Cloudinary"""
        self.stdout.write("\n📦 Migrating Products...")
        
        products = Product.objects.exclude(image='')
        count = 0
        
        for product in products:
            if product.image:
                local_path = str(product.image.path)
                
                # Check if file exists locally
                if os.path.exists(local_path):
                    try:
                        if dry_run:
                            self.stdout.write(
                                f"  Would upload: {product.title} ({local_path})"
                            )
                        else:
                            # Upload to Cloudinary
                            result = cloudinary.uploader.upload(
                                local_path,
                                folder='zone-delivery/products',
                                resource_type='auto'
                            )
                            
                            # Update image field with public_id
                            product.image.name = result['public_id']
                            product.save()
                            
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f"  ✓ {product.title}: {result['public_id']}"
                                )
                            )
                        
                        count += 1
                    
                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(
                                f"  ✗ {product.title}: {str(e)}"
                            )
                        )
        
        self.stdout.write(f"Total Products: {count}")
    
    def migrate_categories(self, dry_run=False):
        """Migrate Category images to Cloudinary"""
        self.stdout.write("\n📂 Migrating Categories...")
        
        categories = Category.objects.exclude(image='')
        count = 0
        
        for category in categories:
            if category.image:
                local_path = str(category.image.path)
                
                if os.path.exists(local_path):
                    try:
                        if dry_run:
                            self.stdout.write(
                                f"  Would upload: {category.name} ({local_path})"
                            )
                        else:
                            result = cloudinary.uploader.upload(
                                local_path,
                                folder='zone-delivery/categories',
                                resource_type='auto'
                            )
                            
                            category.image.name = result['public_id']
                            category.save()
                            
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f"  ✓ {category.name}: {result['public_id']}"
                                )
                            )
                        
                        count += 1
                    
                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(
                                f"  ✗ {category.name}: {str(e)}"
                            )
                        )
        
        self.stdout.write(f"Total Categories: {count}")
    
    def migrate_userprofiles(self, dry_run=False):
        """Migrate UserProfile avatars to Cloudinary"""
        self.stdout.write("\n👤 Migrating User Profiles...")
        
        profiles = UserProfile.objects.exclude(avatar='')
        count = 0
        
        for profile in profiles:
            if profile.avatar:
                local_path = str(profile.avatar.path)
                
                if os.path.exists(local_path):
                    try:
                        if dry_run:
                            self.stdout.write(
                                f"  Would upload: {profile.user.username} ({local_path})"
                            )
                        else:
                            result = cloudinary.uploader.upload(
                                local_path,
                                folder='zone-delivery/profile_pics',
                                resource_type='auto'
                            )
                            
                            profile.avatar.name = result['public_id']
                            profile.save()
                            
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f"  ✓ {profile.user.username}: {result['public_id']}"
                                )
                            )
                        
                        count += 1
                    
                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(
                                f"  ✗ {profile.user.username}: {str(e)}"
                            )
                        )
        
        self.stdout.write(f"Total UserProfiles: {count}")
