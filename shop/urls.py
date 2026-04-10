from django.urls import path
from . import views
from . import admin_views

urlpatterns = [
    # Home & Auth
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # User Profile
    path('profile/', views.profile, name='profile'),
    
    # Orders
    path('my-orders/', views.my_orders, name='my_orders'),
    path('order/<str:order_id>/', views.order_detail, name='order_detail'),
    
    # Shopping Cart
    path('cart/', views.view_cart, name='view_cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart/<int:product_id>/', views.update_cart_quantity, name='update_cart'),
    path('checkout/', views.checkout, name='checkout'),
    
    # Rider
    path('rider/dashboard/', views.rider_dashboard, name='rider_dashboard'),
    path('rider/order/<int:order_id>/', views.rider_order_detail, name='rider_order_detail'),
    
    # Map & Geolocation
    path('map/', views.user_map, name='user_map'),
    path('api/zones/', views.api_zones, name='api_zones'),
    path('api/check-location/', views.api_check_location, name='api_check_location'),
    
    # ============ ADMIN URLS ============
    # Admin Dashboard
    path('admin/', admin_views.admin_dashboard, name='admin_dashboard'),
    
    # Zone Management
    path('admin/zones/', admin_views.admin_zones, name='admin_zones'),
    path('admin/zone/add/', admin_views.admin_zone_add, name='admin_zone_add'),
    path('admin/zone/<int:zone_id>/edit/', admin_views.admin_zone_edit, name='admin_zone_edit'),
    path('admin/zone/<int:zone_id>/delete/', admin_views.admin_zone_delete, name='admin_zone_delete'),
    
    # Category Management
    path('admin/categories/', admin_views.admin_categories, name='admin_categories'),
    path('admin/category/add/', admin_views.admin_category_add, name='admin_category_add'),
    path('admin/category/<int:cat_id>/edit/', admin_views.admin_category_edit, name='admin_category_edit'),
    path('admin/category/<int:cat_id>/delete/', admin_views.admin_category_delete, name='admin_category_delete'),
    
    # Product Management
    path('admin/products/', admin_views.admin_products, name='admin_products'),
    path('admin/product/add/', admin_views.admin_product_add, name='admin_product_add'),
    path('admin/product/<int:prod_id>/edit/', admin_views.admin_product_edit, name='admin_product_edit'),
    path('admin/product/<int:prod_id>/delete/', admin_views.admin_product_delete, name='admin_product_delete'),
    
    # User Management
    path('admin/users/', admin_views.admin_users, name='admin_users'),
    path('admin/user/<int:user_id>/role/', admin_views.admin_user_role_change, name='admin_user_role'),
    
    # Order Management
    path('admin/orders/', admin_views.admin_orders, name='admin_orders'),
    path('admin/order/<str:order_id>/', admin_views.admin_order_detail, name='admin_order_detail'),
    
    # ============ MANAGER PANEL ============
    path('manager/', admin_views.manager_dashboard, name='manager_dashboard'),
    path('manager/order/<int:order_id>/approve/', admin_views.manager_approve_order, name='manager_approve_order'),
    path('manager/order/<int:order_id>/assign-rider/', admin_views.manager_assign_rider, name='manager_assign_rider'),
    
    # Manager Product Management
    path('manager/products/', admin_views.manager_products, name='manager_products'),
    path('manager/product/add/', admin_views.manager_product_add, name='manager_product_add'),
    path('manager/product/<int:prod_id>/edit/', admin_views.manager_product_edit, name='manager_product_edit'),
    path('manager/product/<int:prod_id>/delete/', admin_views.manager_product_delete, name='manager_product_delete'),
    
    # Manager Category Management
    path('manager/categories/', admin_views.manager_categories, name='manager_categories'),
    path('manager/category/add/', admin_views.manager_category_add, name='manager_category_add'),
    path('manager/category/<int:cat_id>/edit/', admin_views.manager_category_edit, name='manager_category_edit'),
    path('manager/category/<int:cat_id>/delete/', admin_views.manager_category_delete, name='manager_category_delete'),
    
    # ============ NOTIFICATION URLS ============
    path('api/notifications/', views.get_notifications, name='get_notifications'),
    path('api/notification/<int:notif_id>/read/', views.mark_notification_read, name='mark_notification_read'),
    path('api/notifications/read-all/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
]
