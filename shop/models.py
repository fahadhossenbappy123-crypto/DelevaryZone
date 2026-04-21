from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal

# User Profile
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('customer', 'গ্রাহক'),
        ('admin', 'অ্যাডমিন'),        # নতুন: Management panel access
        ('rider', 'রাইডার'),
        ('manager', 'ম্যানেজার'),  # অর্ডার গ্রহণ/প্রত্যাখ্যান করতে
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    joined_date = models.DateTimeField(auto_now_add=True)
    is_active_rider = models.BooleanField(default=False)  # Rider status
    
    # নতুন ফিল্ড: Manager এর জন্য
    zone_assigned = models.ForeignKey('Zone', on_delete=models.SET_NULL, null=True, blank=True, 
                                     help_text="যে Zone এর জন্য এই Manager দায়ী")

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"

    class Meta:
        verbose_name_plural = "User Profiles"


# Zone Management
class Zone(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    postal_code = models.CharField(max_length=10, blank=True)
    delivery_charge = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('50.00'))
    
    # Geolocation fields for live location tracking
    latitude = models.FloatField(null=True, blank=True, help_text="Center latitude of service zone")
    longitude = models.FloatField(null=True, blank=True, help_text="Center longitude of service zone")
    radius = models.IntegerField(default=2000, help_text="Service radius in meters (e.g. 2000 = 2km)")
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Zones"


# Category
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    image = models.ImageField(upload_to='category/', blank=True, null=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


# Product
class Product(models.Model):
    UNIT_CHOICES = [
        ('kg', 'কিলোগ্রাম (kg)'),
        ('gram', 'গ্রাম (g)'),
        ('litre', 'লিটার (L)'),
        ('ml', 'মিলিলিটার (ml)'),
        ('piece', 'পিস'),
        ('packet', 'প্যাকেট'),
        ('box', 'বক্স'),
        ('bunch', 'বাঁড়ি/গুচ্ছ'),
        ('dozen', 'ডজন'),
    ]
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default='piece', help_text="পণ্যের ইউনিট")
    image = models.ImageField(upload_to='products/')
    stock = models.PositiveIntegerField(default=50)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.zone.name})" if self.zone else self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Products"


# Order Model
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'অপেক্ষায়'),          # নতুন অর্ডার - Manager এর অপেক্ষায়
        ('approved', 'অনুমোদিত'),        # Manager approved - Rider এর অপেক্ষায়
        ('confirmed', 'নিশ্চিত'),         # Rider assigned
        ('picked', 'রাইডার নিয়েছে'),    # Rider picked up product
        ('delivered', 'ডেলিভার হয়েছে'),  # Delivered
        ('cancelled', 'বাতিল'),           # Rejected or cancelled
    ]

    order_id = models.CharField(max_length=20, unique=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    zone = models.ForeignKey(Zone, on_delete=models.SET_NULL, null=True)
    
    # নতুন: Manager এবং Rider tracking
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                               related_name='managed_orders', 
                               limit_choices_to={'profile__role': 'manager'},
                               help_text="যে Manager এই অর্ডার approve করেছে")
    rider = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                             related_name='deliveries', 
                             limit_choices_to={'profile__role': 'rider'},
                             help_text="যে Rider deliver করবে")
    
    # Customer Details
    customer_phone = models.CharField(max_length=15)
    customer_email = models.EmailField()
    customer_address = models.TextField()
    customer_city = models.CharField(max_length=100)
    
    # Location (Google Maps সাথে capture করা)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    address_formatted = models.TextField(blank=True, null=True, help_text="Google Maps থেকে formatted address")
    
    # Order Info
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_charge = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0'))
    payment_method = models.CharField(max_length=20, default='cash')  # cash, card
    
    # নতুন: Manager approval tracking
    manager_approval_reason = models.TextField(blank=True, null=True, 
                                              help_text="Rejection reason if declined")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    manager_responded_at = models.DateTimeField(blank=True, null=True)
    delivered_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        customer_name = self.customer.username if self.customer else self.customer_phone
        return f"Order {self.order_id} - {customer_name}"

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Orders"


# Order Items
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.title} x{self.quantity}"

    class Meta:
        verbose_name_plural = "Order Items"


# Notification Model
class Notification(models.Model):
    # Simple notification types
    NOTIFICATION_TYPES = [
        ('order_confirmation', 'Order Confirmed'),
        ('order_delivered', 'Order Delivered'),
        ('order_cancelled', 'Order Cancelled'),
        ('rider_assigned', 'Rider Assigned'),
        ('general', 'General'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES, default='general')
    title = models.CharField(max_length=200)
    message = models.TextField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Notifications"
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"
    
    def mark_as_read(self):
        """Mark notification as read"""
        if not self.is_read:
            self.is_read = True
            self.save(update_fields=['is_read'])


# Notification Preferences Model
class NotificationPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_preference')
    order_updates = models.BooleanField(default=True, help_text='Get notified on order status updates')
    order_confirmation = models.BooleanField(default=True, help_text='Get notified when order is confirmed')
    rider_assignments = models.BooleanField(default=True, help_text='Get notified when rider is assigned')
    general_notifications = models.BooleanField(default=True, help_text='Get notified about general updates')
    email_on_order_updates = models.BooleanField(default=True, help_text='Send email on order updates')
    email_on_delivery = models.BooleanField(default=True, help_text='Send email when order is delivered')
    email_on_cancellation = models.BooleanField(default=True, help_text='Send email if order is cancelled')
    email_digests = models.BooleanField(default=False, help_text='Receive daily digest of all notifications')
    enable_sound = models.BooleanField(default=True, help_text='Play sound for new notifications')
    enable_browser_notifications = models.BooleanField(default=True, help_text='Show browser notifications')
    quiet_hours_enabled = models.BooleanField(default=False, help_text='Enable quiet hours (no notifications)')
    quiet_hours_start = models.TimeField(null=True, blank=True, help_text='Quiet hours start time (HH:MM)')
    quiet_hours_end = models.TimeField(null=True, blank=True, help_text='Quiet hours end time (HH:MM)')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Notification Preferences'

    def __str__(self):
        return f"Preferences for {self.user.username}"


# Hero Slide Model - For Homepage Carousel
class HeroSlide(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500, blank=True)
    button_text = models.CharField(max_length=100, default="Order Now")
    button_link = models.CharField(max_length=300, default="/register/", help_text="URL to navigate when button is clicked")
    background_image = models.ImageField(upload_to='hero_slides/')
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text="Display order of slides")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order']
        verbose_name_plural = "Hero Slides"
    
    def __str__(self):
        return f"{self.title} (Order: {self.order})"
