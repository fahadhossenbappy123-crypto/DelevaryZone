from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from decouple import config

from shop.models import UserProfile


class Command(BaseCommand):
    help = 'Create or synchronize the default admin user configured by .env values.'

    def handle(self, *args, **options):
        create_default = config('ADMIN_CREATE_DEFAULT', default=False, cast=bool)
        username = config('ADMIN_USERNAME', default=None)
        password = config('ADMIN_PASSWORD', default=None)
        email = config('ADMIN_EMAIL', default='admin@example.com')

        if not create_default:
            self.stdout.write(self.style.NOTICE('ADMIN_CREATE_DEFAULT is disabled. No admin user was created.'))
            return

        if not username or not password:
            self.stderr.write(self.style.ERROR('ADMIN_USERNAME and ADMIN_PASSWORD must be set to create the default admin user.'))
            return

        User = get_user_model()
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'is_staff': True,
                'is_superuser': True,
                'is_active': True,
            },
        )

        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Created admin user "{username}".'))
        else:
            modified = False
            if not user.is_staff:
                user.is_staff = True
                modified = True
            if not user.is_superuser:
                user.is_superuser = True
                modified = True
            if not user.is_active:
                user.is_active = True
                modified = True
            if email and user.email != email:
                user.email = email
                modified = True
            user.set_password(password)
            if modified:
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Updated admin user "{username}".'))
            else:
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Admin user "{username}" already exists and password was updated.'))

        profile, _ = UserProfile.objects.get_or_create(user=user)
        if profile.role != 'admin':
            profile.role = 'admin'
            profile.save()
            self.stdout.write(self.style.SUCCESS(f'Assigned admin role for "{username}".'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Admin role already assigned for "{username}".'))
