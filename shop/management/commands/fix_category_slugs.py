from django.core.management.base import BaseCommand
from shop.models import Category

class Command(BaseCommand):
    help = 'Check and fix category slugs'

    def handle(self, *args, **options):
        categories = Category.objects.all()
        self.stdout.write(f"Found {len(categories)} categories:")
        
        for cat in categories:
            self.stdout.write(f"  ID: {cat.id}, Name: '{cat.name}', Slug: '{cat.slug}'")
            
            if not cat.slug:
                self.stdout.write(f"    -> Missing slug, fixing...")
                cat.save()  # This should trigger the save method to generate slug
                self.stdout.write(f"    -> Fixed slug: '{cat.slug}'")
            elif cat.slug == 'category' or cat.slug.startswith('category-'):
                self.stdout.write(f"    -> Bad slug detected, regenerating...")
                # Force regeneration by clearing slug
                cat.slug = ''
                cat.save()
                self.stdout.write(f"    -> New slug: '{cat.slug}'")