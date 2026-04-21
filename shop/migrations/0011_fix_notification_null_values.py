# Migration to fix existing notification records with default values

from django.db import migrations


def set_default_values(apps, schema_editor):
    """Set default values for new fields in existing notifications"""
    Notification = apps.get_model('shop', 'Notification')
    
    # Update all existing notifications that have NULL values
    Notification.objects.filter(email_sent__isnull=True).update(email_sent=False)
    Notification.objects.filter(is_deleted__isnull=True).update(is_deleted=False)


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_notification_enhancements'),
    ]

    operations = [
        migrations.RunPython(set_default_values),
    ]
