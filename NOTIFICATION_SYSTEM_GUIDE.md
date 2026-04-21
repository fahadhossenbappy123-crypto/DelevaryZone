# ZoneDelivery Notification System - Improvements Guide

## Overview

The notification system has been significantly enhanced to provide a better user experience with more control, flexibility, and reliability.

## What's New

### 1. **Enhanced Notification Model**
- Added `email_sent` field to track sent emails
- Added `is_deleted` field for soft deletion
- Added `read_at` timestamp to know when user read the notification
- Added database indexes for faster queries
- New `mark_as_read()` method on Notification model

### 2. **Notification Preference Model**
Users can now customize how they receive notifications:
- **In-App Notifications**: Control what types of alerts to see
- **Email Notifications**: Choose which events trigger emails
- **Sound & Browser Notifications**: Toggle sound alerts and browser notifications
- **Quiet Hours**: Set time ranges when notifications should be silent

### 3. **Notification Service Module** (`notification_service.py`)
Core service for handling notification creation and delivery:

```python
# Create a notification with all checks
create_notification(
    user=customer,
    notification_type='order_delivered',
    title='Order Delivered 🎉',
    message='Your order has been delivered',
    order=order,
    send_email=True
)

# Get notifications with filtering
get_notifications(user, limit=10, skip_deleted=True)

# Get unread count
get_unread_count(user)

# Delete/archive notifications
delete_notification(notification)
clear_all_notifications(user)

# Handle order status changes automatically
update_order_notifications(order, 'delivered')
```

### 4. **New Notification Types**
Extended notification types for better granularity:
- `order_confirmation` - Order successfully placed
- `order_processing` - Order approved by manager
- `order_picked` - Rider picked up the order
- `order_in_transit` - Order is on the way
- `order_delivered` - Order delivered to customer
- `order_cancelled` - Order was cancelled
- `rider_assigned` - Rider assigned to delivery
- `rider_near` - Rider is close to delivery location
- `payment_reminder` - Payment reminder
- `general` - General announcements

### 5. **Email Notification Support**
Automatic email notifications with:
- HTML email templates
- Selective email sending based on user preferences
- Integration with Django's email backend
- Configurable per notification type

### 6. **Notification History Page** (`/notifications/`)
New page showing:
- Complete notification history
- Pagination support (20 per page)
- Notification type indicators with colors and icons
- View order details from notification
- Delete individual notifications
- Clear all notifications

### 7. **Notification Preferences Page** (`/notifications/preferences/`)
User-friendly settings panel for:
- In-app notification preferences
- Email notification preferences
- Sound and browser notifications
- Quiet hours configuration

## API Endpoints

### Get Notifications
```
GET /api/notifications/
```
Returns JSON with list of last 10 notifications and unread count.

### Mark Single Notification as Read
```
POST /api/notification/{notif_id}/read/
```

### Mark All as Read
```
POST /api/notifications/read-all/
```

### Delete Notification
```
POST /api/notification/{notif_id}/delete/
```

### Clear All Notifications
```
POST /api/notifications/clear/
```

## Configuration

### Email Settings
Update your `settings.py`:

```python
# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-password'
DEFAULT_FROM_EMAIL = 'noreply@zonedelivery.com'
```

### Notification Service Configuration
The service automatically:
1. Checks user preferences before creating notifications
2. Respects quiet hours
3. Sends emails based on user preferences
4. Creates soft deletes instead of hard deletes

## Usage Examples

### In Views - When Order Status Changes
```python
from .notification_service import update_order_notifications

# After changing order status
order.status = 'delivered'
order.save()

# This automatically creates notifications for customer and rider
update_order_notifications(order, 'delivered')
```

### Creating Custom Notifications
```python
from .notification_service import create_notification

create_notification(
    user=user,
    notification_type='general',
    title='Special Offer!',
    message='Get 20% off on your next order',
)
```

### Batch Operations
```python
from .notification_service import create_batch_notifications

users = User.objects.filter(profile__role='customer')
notifications = create_batch_notifications(
    users=users,
    notification_type='general',
    title='Maintenance Notice',
    message='System will be down for 1 hour',
)
```

## Database Migrations

Run these commands to apply the new models:

```bash
python manage.py makemigrations
python manage.py migrate
```

Migration file: `0010_notification_enhancements.py`

Changes:
- Adds 3 new fields to Notification model
- Creates NotificationPreference model
- Adds 2 database indexes for performance
- Adds new notification types

## Frontend Integration

### JavaScript for Browser Notifications
The notification modal now includes:
- Links to history page
- Link to preferences
- Delete individual notifications
- Clear all functionality

### Enhanced Notification Icons
Each notification type has:
- Unique icon
- Color indicator
- Status badge

## Performance Considerations

### Database Indexes
Added indexes on:
- `(user, -created_at)` - For fetching user's notifications quickly
- `(user, is_read)` - For counting unread notifications

### Query Optimization
- Uses `select_related()` for foreign keys
- Soft deletes avoid actual deletions
- Efficient pagination support

## Future Enhancements

Potential improvements:
1. WebSocket support for real-time notifications (instead of polling)
2. SMS notifications for critical updates
3. Push notifications for mobile apps
4. Notification templates/builder UI
5. Notification scheduling
6. Analytics dashboard for notification metrics
7. A/B testing framework for notification content

## Troubleshooting

### Emails Not Sending
1. Check email configuration in `settings.py`
2. Verify SMTP credentials
3. Check `email_sent` field in Notification model
4. Review Django logs for errors

### Notifications Not Appearing
1. Check user's NotificationPreference settings
2. Verify quiet hours are not active
3. Check `is_deleted` field
4. Verify notification_type is correct

### Missing NotificationPreference
Auto-created when user tries to set preferences:
```python
prefs, created = NotificationPreference.objects.get_or_create(user=user)
```

## Files Modified/Created

**New Files:**
- `shop/notification_service.py` - Core notification service
- `shop/templates/shop/notification_history.html` - History page
- `shop/templates/shop/notification_preferences.html` - Settings page
- `shop/templates/shop/email/notification_email.html` - Email template
- `shop/migrations/0010_notification_enhancements.py` - Migration

**Modified Files:**
- `shop/models.py` - Enhanced Notification + new NotificationPreference
- `shop/views.py` - New notification views + imports
- `shop/admin_views.py` - Updated imports
- `shop/urls.py` - New URL patterns
- `shop/templates/shop/base.html` - Updated notification modal footer

## Testing

To test the notification system:

1. **Create a notification**
   ```python
   from shop.notification_service import create_notification
   from django.contrib.auth.models import User
   
   user = User.objects.first()
   create_notification(
       user=user,
       notification_type='general',
       title='Test',
       message='This is a test',
   )
   ```

2. **Check API endpoint**
   Visit `/api/notifications/` when logged in

3. **View history**
   Visit `/notifications/` in the browser

4. **Test preferences**
   Visit `/notifications/preferences/`

## Support

For issues or questions about the notification system, check:
- Notification model: `shop/models.py`
- Service logic: `shop/notification_service.py`
- View logic: `shop/views.py`
- API responses in browser console (F12)
