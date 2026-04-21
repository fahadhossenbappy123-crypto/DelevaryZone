# Generated migration for NotificationPreference model and enhanced Notification model

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_product_unit'),
    ]

    operations = [
        # Add fields to Notification model
        migrations.AddField(
            model_name='notification',
            name='email_sent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='notification',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='notification',
            name='read_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        
        # Add new notification types
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(
                choices=[
                    ('order_confirmation', 'Order Confirmed'),
                    ('order_processing', 'Order Processing'),
                    ('order_picked', 'Order Picked'),
                    ('order_in_transit', 'Order In Transit'),
                    ('order_delivered', 'Order Delivered'),
                    ('order_cancelled', 'Order Cancelled'),
                    ('rider_assigned', 'Rider Assigned'),
                    ('rider_near', 'Rider Near You'),
                    ('payment_reminder', 'Payment Reminder'),
                    ('general', 'General'),
                ],
                default='general',
                max_length=50,
            ),
        ),
        
        # Add indexes to Notification model
        migrations.AddIndex(
            model_name='notification',
            index=models.Index(fields=['user', '-created_at'], name='shop_notifi_user_id_created_idx'),
        ),
        migrations.AddIndex(
            model_name='notification',
            index=models.Index(fields=['user', 'is_read'], name='shop_notifi_user_id_is_read_idx'),
        ),
        
        # Create NotificationPreference model
        migrations.CreateModel(
            name='NotificationPreference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_updates', models.BooleanField(default=True, help_text='Get notified on order status updates')),
                ('order_confirmation', models.BooleanField(default=True, help_text='Get notified when order is confirmed')),
                ('rider_assignments', models.BooleanField(default=True, help_text='Get notified when rider is assigned')),
                ('general_notifications', models.BooleanField(default=True, help_text='Get notified about general updates')),
                ('email_on_order_updates', models.BooleanField(default=True, help_text='Send email on order updates')),
                ('email_on_delivery', models.BooleanField(default=True, help_text='Send email when order is delivered')),
                ('email_on_cancellation', models.BooleanField(default=True, help_text='Send email if order is cancelled')),
                ('email_digests', models.BooleanField(default=False, help_text='Receive daily digest of all notifications')),
                ('enable_sound', models.BooleanField(default=True, help_text='Play sound for new notifications')),
                ('enable_browser_notifications', models.BooleanField(default=True, help_text='Show browser notifications')),
                ('quiet_hours_enabled', models.BooleanField(default=False, help_text='Enable quiet hours (no notifications)')),
                ('quiet_hours_start', models.TimeField(blank=True, help_text='Quiet hours start time (HH:MM)', null=True)),
                ('quiet_hours_end', models.TimeField(blank=True, help_text='Quiet hours end time (HH:MM)', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='notification_preference', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Notification Preferences',
            },
        ),
    ]
