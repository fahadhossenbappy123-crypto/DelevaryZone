#!/usr/bin/env python
"""
Create initial admin user if not exists
Run this during deployment: python manage.py create_admin_user
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Create initial admin user if it does not exist'

    def handle(self, *args, **options):
        # Admin credentials (can be changed in this file)
        ADMIN_USERNAME = 'adminbappy'
        ADMIN_EMAIL = 'admin@zonedelivery.com'
        ADMIN_PASSWORD = 'bappy8800'

        # Check if admin user already exists
        if User.objects.filter(username=ADMIN_USERNAME).exists():
            self.stdout.write(
                self.style.WARNING(f'Admin user "{ADMIN_USERNAME}" already exists')
            )
            return

        # Create superuser
        try:
            User.objects.create_superuser(
                username=ADMIN_USERNAME,
                email=ADMIN_EMAIL,
                password=ADMIN_PASSWORD
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created admin user:\n'
                    f'  Username: {ADMIN_USERNAME}\n'
                    f'  Email: {ADMIN_EMAIL}\n'
                    f'  Password: {ADMIN_PASSWORD}'
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating admin user: {str(e)}')
            )
