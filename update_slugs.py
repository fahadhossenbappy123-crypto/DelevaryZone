#!/usr/bin/env python
"""
স্ক্রিপ্ট যা সব Category এর slug পূরণ করে
"""
import os
import django

# Django সেটআপ
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zonedelivery.settings')
django.setup()

from django.utils.text import slugify
from shop.models import Category

print("Category slugs আপডেট করছি...")
print("-" * 50)

for cat in Category.objects.all():
    if not cat.slug:
        cat.slug = slugify(cat.name)
        cat.save()
        print(f"✅ আপডেট করা হয়েছে: {cat.name} -> {cat.slug}")
    else:
        print(f"✓ ইতিমধ্যে আছে: {cat.name} -> {cat.slug}")

print("-" * 50)
print("সম্পন্ন!")
