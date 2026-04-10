from django.contrib import admin
from .models import UserProfile, Zone, Category, Product, Order, OrderItem, Notification

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'phone', 'joined_date']
    list_filter = ['role', 'joined_date']
    search_fields = ['user__username', 'phone']

@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ['name', 'postal_code', 'delivery_charge', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'zone', 'price', 'stock', 'is_available']
    list_filter = ['is_available', 'category', 'zone', 'created_at']
    search_fields = ['title', 'description']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'customer', 'zone', 'status', 'total_amount', 'created_at']
    list_filter = ['status', 'created_at', 'zone']
    search_fields = ['order_id', 'customer__username', 'customer_phone']
    readonly_fields = ['order_id', 'created_at', 'updated_at']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price']
    search_fields = ['order__order_id', 'product__title']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'notification_type', 'title', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['user__username', 'title', 'message']
    readonly_fields = ['created_at']
