from django.core.management.base import BaseCommand
from shop.models import Category

class Command(BaseCommand):
    help = 'Check category slugs'

    def handle(self, *args, **options):
        categories = Category.objects.all()
        self.stdout.write(f'Total categories: {categories.count()}')
        
        for cat in categories:
            self.stdout.write(f'ID: {cat.id}, Name: "{cat.name}", Slug: "{cat.slug}"')
            
            # If slug is empty, generate it
            if not cat.slug:
                from django.utils.text import slugify
                cat.slug = slugify(cat.name)
                cat.save()
                self.stdout.write(f'  -> Generated slug: "{cat.slug}"')