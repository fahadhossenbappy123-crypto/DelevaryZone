from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from django.conf import settings
from .models import UserProfile, Zone, Category, Product, Order, OrderItem, Notification, HeroSlide, NotificationPreference
from .forms import UserRegisterForm, UserProfileForm
from .notification_service import create_notification, update_order_notifications
import json


def is_admin(user):
    """Check if user is admin"""
    # Check Django's built-in is_staff/is_superuser OR custom admin role
    if user.is_staff or user.is_superuser:
        return True
    # Check if user has admin role in UserProfile
    try:
        return user.profile.role == 'admin'
    except:
        return False


# ============ ADMIN DASHBOARD ============
@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_dashboard(request):
    """Admin Dashboard Home"""
    total_users = User.objects.count()
    total_riders = UserProfile.objects.filter(role='rider').count()
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    completed_orders = Order.objects.filter(status='delivered').count()
    
    recent_orders = Order.objects.order_by('-created_at')[:5]
    
    context = {
        'total_users': total_users,
        'total_riders': total_riders,
        'total_products': total_products,
        'total_orders': total_orders,
        'completed_orders': completed_orders,
        'recent_orders': recent_orders,
    }
    return render(request, 'shop/admin/dashboard.html', context)


# ============ ZONE MANAGEMENT ============
@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_zones(request):
    """Zone List"""
    zones = Zone.objects.all()
    
    context = {'zones': zones}
    return render(request, 'shop/admin/zones.html', context)


@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_zone_add(request):
    """Add Zone with Map"""
    if request.method == 'POST':
        name = request.POST.get('name')
        postal_code = request.POST.get('postal_code')
        delivery_charge = request.POST.get('delivery_charge')
        description = request.POST.get('description')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        radius = request.POST.get('radius', 2000)
        
        if Zone.objects.filter(name=name).exists():
            messages.error(request, 'এই নাম ইতিমধ্যে ব্যবহৃত হয়েছে।')
        else:
            try:
                zone = Zone.objects.create(
                    name=name,
                    postal_code=postal_code,
                    delivery_charge=delivery_charge,
                    description=description,
                    latitude=float(latitude) if latitude else None,
                    longitude=float(longitude) if longitude else None,
                    radius=int(radius)
                )
                messages.success(request, f'Zone "{name}" যোগ করা হয়েছে।')
                return redirect('admin_zones')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
    
    return render(request, 'shop/admin/zone_form.html')


@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_zone_edit(request, zone_id):
    """Edit Zone with Map"""
    zone = get_object_or_404(Zone, id=zone_id)
    
    if request.method == 'POST':
        zone.name = request.POST.get('name')
        zone.postal_code = request.POST.get('postal_code')
        zone.delivery_charge = request.POST.get('delivery_charge')
        zone.description = request.POST.get('description')
        zone.is_active = request.POST.get('is_active') == 'on'
        
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        radius = request.POST.get('radius', 2000)
        
        if latitude:
            zone.latitude = float(latitude)
        if longitude:
            zone.longitude = float(longitude)
        if radius:
            zone.radius = int(radius)
        
        zone.save()
        
        messages.success(request, f'Zone "{zone.name}" আপডেট হয়েছে।')
        return redirect('admin_zones')
    
    context = {'zone': zone}
    return render(request, 'shop/admin/zone_form.html', context)


@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_zone_delete(request, zone_id):
    """Delete Zone"""
    zone = get_object_or_404(Zone, id=zone_id)
    zone.delete()
    messages.success(request, f'Zone "{zone.name}" ডিলিট করা হয়েছে।')
    return redirect('admin_zones')


# ============ CATEGORY MANAGEMENT ============
@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_categories(request):
    """Category List"""
    categories = Category.objects.all()
    
    context = {'categories': categories}
    return render(request, 'shop/admin/categories.html', context)


@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_category_add(request):
    """Add Category"""
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        
        if Category.objects.filter(name=name).exists():
            messages.error(request, 'এই নাম ইতিমধ্যে ব্যবহৃত হয়েছে।')
        else:
            from django.utils.text import slugify
            slug = slugify(name)
            Category.objects.create(
                name=name,
                slug=slug,
                description=description,
                image=image
            )
            messages.success(request, f'Category "{name}" যোগ করা হয়েছে।')
            return redirect('admin_categories')
    
    return render(request, 'shop/admin/category_form.html')


@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_category_edit(request, cat_id):
    """Edit Category"""
    category = get_object_or_404(Category, id=cat_id)
    
    if request.method == 'POST':
        category.name = request.POST.get('name')
        category.description = request.POST.get('description')
        if request.FILES.get('image'):
            category.image = request.FILES.get('image')
        category.save()
        
        messages.success(request, f'Category "{category.name}" আপডেট হয়েছে।')
        return redirect('admin_categories')
    
    context = {'category': category}
    return render(request, 'shop/admin/category_form.html', context)


@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_category_delete(request, cat_id):
    """Delete Category"""
    category = get_object_or_404(Category, id=cat_id)
    category.delete()
    messages.success(request, f'Category "{category.name}" ডিলিট করা হয়েছে।')
    return redirect('admin_categories')


# ============ PRODUCT MANAGEMENT ============
@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_products(request):
    """Product List"""
    products = Product.objects.all().select_related('category', 'zone')
    
    # Filters
    category = request.GET.get('category')
    zone = request.GET.get('zone')
    search = request.GET.get('search')
    
    if category:
        products = products.filter(category_id=category)
    if zone:
        products = products.filter(zone_id=zone)
    if search:
        products = products.filter(Q(title__icontains=search) | Q(description__icontains=search))
    
    categories = Category.objects.all()
    zones = Zone.objects.all()
    
    context = {
        'products': products,
        'categories': categories,
        'zones': zones,
    }
    return render(request, 'shop/admin/products.html', context)


@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_product_add(request):
    """Add Product"""
    if request.method == 'POST':
        category_id = request.POST.get('category')
        zone_id = request.POST.get('zone')
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        unit = request.POST.get('unit')
        stock = request.POST.get('stock')
        image = request.FILES.get('image')
        
        try:
            category = Category.objects.get(id=category_id)
            zone = Zone.objects.get(id=zone_id)
            
            Product.objects.create(
                category=category,
                zone=zone,
                title=title,
                description=description,
                price=price,
                unit=unit,
                stock=stock,
                image=image
            )
            messages.success(request, f'Product "{title}" যোগ করা হয়েছে।')
            return redirect('admin_products')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    categories = Category.objects.all()
    zones = Zone.objects.all()
    
    context = {'categories': categories, 'zones': zones, 'unit_choices': Product.UNIT_CHOICES}
    return render(request, 'shop/admin/product_form.html', context)


@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_product_edit(request, prod_id):
    """Edit Product"""
    product = get_object_or_404(Product, id=prod_id)
    
    if request.method == 'POST':
        product.category_id = request.POST.get('category')
        product.zone_id = request.POST.get('zone')
        product.title = request.POST.get('title')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        product.unit = request.POST.get('unit')
        product.stock = request.POST.get('stock')
        product.is_available = request.POST.get('is_available') == 'on'
        
        if request.FILES.get('image'):
            product.image = request.FILES.get('image')
        
        product.save()
        messages.success(request, f'Product "{product.title}" আপডেট হয়েছে।')
        return redirect('admin_products')
    
    categories = Category.objects.all()
    zones = Zone.objects.all()
    
    context = {
        'product': product,
        'categories': categories,
        'zones': zones,
        'unit_choices': Product.UNIT_CHOICES,
    }
    return render(request, 'shop/admin/product_form.html', context)


@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_product_delete(request, prod_id):
    """Delete Product"""
    product = get_object_or_404(Product, id=prod_id)
    product.delete()
    messages.success(request, f'Product "{product.title}" ডিলিট করা হয়েছে।')
    return redirect('admin_products')


# ============ USER MANAGEMENT ============
@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_users(request):
    """User List"""
    users = User.objects.all().prefetch_related('profile')
    
    # Filter
    role = request.GET.get('role')
    search = request.GET.get('search')
    
    if role:
        users = users.filter(profile__role=role)
    if search:
        users = users.filter(Q(username__icontains=search) | Q(email__icontains=search))
    
    context = {'users': users}
    return render(request, 'shop/admin/users.html', context)


@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_user_role_change(request, user_id):
    """Change User Role"""
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        new_role = request.POST.get('role')
        zone_id = request.POST.get('zone')
        
        user.profile.role = new_role
        user.profile.is_active_rider = (new_role == 'rider')
        
        # If manager role, assign zone
        if new_role == 'manager':
            if zone_id:
                zone = Zone.objects.get(id=zone_id)
                user.profile.zone_assigned = zone
            else:
                messages.error(request, 'ম্যানেজারের জন্য জোন নির্বাচন করুন।')
                zones = Zone.objects.all()
                context = {
                    'user': user,
                    'ROLE_CHOICES': [('customer', 'গ্রাহক'), ('rider', 'রাইডার'), ('manager', 'ম্যানেজার')],
                    'zones': zones,
                }
                return render(request, 'shop/admin/user_role.html', context)
        else:
            user.profile.zone_assigned = None
        
        user.profile.save()
        
        messages.success(request, f'{user.username} এর ভূমিকা "{user.profile.get_role_display()}" এ পরিবর্তন করা হয়েছে।')
        return redirect('admin_users')
    
    zones = Zone.objects.all()
    context = {
        'user': user,
        'ROLE_CHOICES': [('customer', 'গ্রাহক'), ('rider', 'রাইডার'), ('manager', 'ম্যানেজার')],
        'zones': zones,
    }
    return render(request, 'shop/admin/user_role.html', context)


@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_orders(request):
    """Order List"""
    orders = Order.objects.all().select_related('customer', 'zone', 'rider')
    
    # Filter
    status = request.GET.get('status')
    zone = request.GET.get('zone')
    
    if status:
        orders = orders.filter(status=status)
    if zone:
        orders = orders.filter(zone_id=zone)
    
    zones = Zone.objects.all()
    status_choices = Order._meta.get_field('status').choices
    
    # Serialize orders to JSON for JavaScript
    orders_json = json.dumps([
        {
            'order_id': order.order_id,
            'latitude': float(order.latitude) if order.latitude else None,
            'longitude': float(order.longitude) if order.longitude else None,
            'status': order.status,
            'customer_address': order.customer_address or '',
            'zone': order.zone.name if order.zone else '',
            'customer': order.customer.username if order.customer else '',
            'total_amount': str(order.total_amount),
            'rider': order.rider.username if order.rider else '',
            'phone_number': order.customer.profile.phone_number if order.customer else ''
        }
        for order in orders
    ])
    
    context = {
        'orders': orders,
        'orders_json': orders_json,
        'zones': zones,
        'status_choices': status_choices,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
    }
    return render(request, 'shop/admin/orders.html', context)


@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_order_detail(request, order_id):
    """Order Detail"""
    order = get_object_or_404(Order, order_id=order_id)
    items = order.items.all()
    
    if request.method == 'POST':
        status = request.POST.get('status')
        rider_id = request.POST.get('rider')
        
        order.status = status
        if rider_id:
            order.rider_id = rider_id
        order.save()
        
        messages.success(request, 'অর্ডার আপডেট করা হয়েছে।')
        return redirect('admin_orders')
    
    riders = User.objects.filter(profile__role='rider')
    status_choices = Order._meta.get_field('status').choices
    
    # Get zone information for map display
    zone = order.zone
    zone_data = None
    if zone:
        zone_data = {
            'id': zone.id,
            'name': zone.name,
            'latitude': zone.latitude,
            'longitude': zone.longitude,
            'radius': zone.radius,
        }
    
    context = {
        'order': order,
        'items': items,
        'riders': riders,
        'status_choices': status_choices,
        'zone_data': zone_data,
    }
    return render(request, 'shop/admin/order_detail.html', context)


# ================ MANAGER PANEL ================
def is_manager(user):
    """Check if user is a manager"""
    return hasattr(user, 'profile') and user.profile.role == 'manager'


@login_required(login_url='login')
@user_passes_test(is_manager)
def manager_dashboard(request):
    """Manager Dashboard - Orders to Approve"""
    from django.utils import timezone
    
    try:
        manager = request.user.profile
        
        # Check if manager has a zone assigned
        if not manager.zone_assigned:
            messages.error(request, 'আপনার কোনো জোন নির্ধারিত হয়নি। Admin এর সাথে যোগাযোগ করুন।')
            return redirect('home')
        
        # Pending orders in manager's zone
        pending_orders = Order.objects.filter(
            status='pending',
            zone=manager.zone_assigned
        ).select_related('customer', 'zone').order_by('-created_at')
        
        # Approved orders (awaiting rider assignment)
        approved_orders = Order.objects.filter(
            status='approved',
            manager=request.user,
            rider__isnull=True
        ).select_related('customer', 'zone')
        
        # Active deliveries (rider assigned)
        active_orders = Order.objects.filter(
            manager=request.user,
            status__in=['confirmed', 'picked']
        ).select_related('customer', 'zone', 'rider').order_by('-updated_at')
        
        # Completed orders
        completed_orders_qs = Order.objects.filter(
            manager=request.user,
            status='delivered'
        ).select_related('customer', 'zone', 'rider').order_by('-delivered_at')
        
        # Statistics
        today_completed = completed_orders_qs.filter(
            delivered_at__date=timezone.now().date()
        ).count()
        
        # Get last 10 completed orders for display
        completed_orders = completed_orders_qs[:10]
        
        context = {
            'manager': manager,
            'pending_orders': pending_orders,
            'approved_orders': approved_orders,
            'active_orders': active_orders,
            'completed_orders': completed_orders,
            'today_completed': today_completed,
            'pending_count': pending_orders.count(),
            'active_count': active_orders.count(),
        }
        return render(request, 'shop/manager/dashboard.html', context)
    
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        return redirect('home')


@login_required(login_url='login')
@user_passes_test(is_manager)
def manager_approve_order(request, order_id):
    """Manager approves or rejects an order"""
    order = get_object_or_404(Order, id=order_id)
    manager = request.user.profile
    
    # Verify order is in manager's zone
    if order.zone != manager.zone_assigned:
        messages.error(request, 'আপনার এই অর্ডার approve করার অনুমতি নেই।')
        return redirect('manager_dashboard')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'approve':
            order.status = 'approved'
            order.manager = request.user
            order.manager_responded_at = timezone.now()
            order.save()
            
            # Create notification for customer with email
            if order.customer:
                create_notification(
                    user=order.customer,
                    notification_type='order_processing',
                    title='Order Approved ✓',
                    message=f'Your order #{order.order_id} has been approved. Rider will be assigned soon.',
                    order=order,
                    send_email=True
                )
            
            messages.success(request, f'অর্ডার {order.order_id} অনুমোদিত হয়েছে। এখন রাইডার নির্ধারণ করুন।')
            
        elif action == 'reject':
            reason = request.POST.get('reason', '')
            order.status = 'cancelled'
            order.manager = request.user
            order.manager_approval_reason = reason
            order.manager_responded_at = timezone.now()
            order.save()
            
            # Create notification for customer with email
            if order.customer:
                create_notification(
                    user=order.customer,
                    notification_type='order_cancelled',
                    title='Order Cancelled ✗',
                    message=f'Your order #{order.order_id} has been cancelled. Reason: {reason}',
                    order=order,
                    send_email=True
                )
            
            messages.info(request, f'অর্ডার {order.order_id} প্রত্যাখ্যান করা হয়েছে।')
        
        return redirect('manager_dashboard')
    
    # Get items with calculated totals
    items = order.items.all()
    for item in items:
        item.item_total = item.quantity * item.price
    
    context = {
        'order': order,
        'items': items,
    }
    return render(request, 'shop/manager/approve_order.html', context)


@login_required(login_url='login')
@user_passes_test(is_manager)
def manager_assign_rider(request, order_id):
    """Manager assigns a rider to an approved order"""
    order = get_object_or_404(Order, id=order_id)
    manager = request.user.profile
    
    # Verify
    if order.zone != manager.zone_assigned or order.status != 'approved':
        messages.error(request, 'এই অর্ডারের জন্য রাইডার নির্ধারণ করা সম্ভব নয়।')
        return redirect('manager_dashboard')
    
    if request.method == 'POST':
        rider_id = request.POST.get('rider_id')
        
        try:
            rider = User.objects.get(id=rider_id, profile__role='rider')
            order.rider = rider
            order.status = 'confirmed'
            order.save()
            messages.success(request, f'রাইডার {rider.username} কে অর্ডার নির্ধারণ করা হয়েছে।')
            
            # Create notification for customer
            if order.customer:
                create_notification(
                    user=order.customer,
                    notification_type='rider_assigned',
                    title='Rider Assigned',
                    message=f'Rider {rider.first_name or rider.username} has been assigned to your order #{order.order_id}.',
                    order=order
                )
            
            # Create notification for rider
            create_notification(
                user=rider,
                notification_type='order_picked',
                title='New Order Assigned',
                message=f'Order #{order.order_id} has been assigned to you for delivery.',
                order=order
            )
        except User.DoesNotExist:
            messages.error(request, 'অমান্য রাইডার নির্বাচন।')
        
        return redirect('manager_dashboard')
    
    # Get available riders
    riders = User.objects.filter(
        profile__role='rider',
        profile__is_active_rider=True
    ).order_by('username')
    
    # Get items with calculated totals
    items = order.items.all()
    for item in items:
        item.item_total = item.quantity * item.price
    
    context = {
        'order': order,
        'riders': riders,
        'items': items,
    }
    return render(request, 'shop/manager/assign_rider.html', context)


@login_required(login_url='login')
@user_passes_test(is_manager)
def manager_riders(request):
    """Manager views and manages riders for their zone"""
    from django.db.models import Count, Q, F
    from django.utils import timezone
    
    manager = request.user.profile
    
    # Get all active riders in the system (managers can see all riders)
    riders = User.objects.filter(
        profile__role='rider'
    ).select_related('profile').prefetch_related('orders_as_rider')
    
    # Annotate riders with statistics
    riders = riders.annotate(
        total_deliveries=Count('orders_as_rider', filter=Q(orders_as_rider__status='delivered')),
        pending_orders=Count('orders_as_rider', filter=Q(orders_as_rider__status__in=['confirmed', 'picked'])),
        cancelled_orders=Count('orders_as_rider', filter=Q(orders_as_rider__status='cancelled'))
    ).order_by('-profile__is_active_rider', 'username')
    
    # Calculate additional stats for each rider
    rider_list = []
    for rider in riders:
        delivered_today = rider.orders_as_rider.filter(
            status='delivered',
            delivered_at__date=timezone.now().date()
        ).count()
        
        # Get average delivery time
        completed_orders = rider.orders_as_rider.filter(status='delivered')
        avg_delivery_time = None
        if completed_orders.exists():
            total_time = sum([
                (order.delivered_at - order.updated_at).total_seconds() 
                for order in completed_orders if order.delivered_at and order.updated_at
            ])
            avg_delivery_time = int(total_time / completed_orders.count() / 60) if total_time else None
        
        rider_list.append({
            'user': rider,
            'profile': rider.profile,
            'total_deliveries': rider.total_deliveries,
            'pending_orders': rider.pending_orders,
            'cancelled_orders': rider.cancelled_orders,
            'delivered_today': delivered_today,
            'avg_delivery_time': avg_delivery_time,
            'is_active': rider.profile.is_active_rider,
        })
    
    # Search/Filter
    search = request.GET.get('search')
    status_filter = request.GET.get('status')  # 'active' or 'inactive'
    
    if search:
        rider_list = [r for r in rider_list if search.lower() in r['user'].username.lower() or 
                      (r['profile'].phone and search in r['profile'].phone)]
    
    if status_filter == 'active':
        rider_list = [r for r in rider_list if r['is_active']]
    elif status_filter == 'inactive':
        rider_list = [r for r in rider_list if not r['is_active']]
    
    context = {
        'riders': rider_list,
        'manager': manager,
        'search': search,
        'status_filter': status_filter,
    }
    return render(request, 'shop/manager/riders.html', context)


# ================ MANAGER PRODUCTS ================
@login_required(login_url='login')
@user_passes_test(is_manager)
def manager_products(request):
    """Manager can view and manage products for their zone"""
    manager = request.user.profile
    products = Product.objects.filter(zone=manager.zone_assigned).select_related('category', 'zone')
    
    # Search
    search = request.GET.get('search')
    if search:
        products = products.filter(Q(title__icontains=search) | Q(description__icontains=search))
    
    context = {
        'products': products,
        'manager': manager,
    }
    return render(request, 'shop/manager/products.html', context)


@login_required(login_url='login')
@user_passes_test(is_manager)
def manager_product_add(request):
    """Manager adds product to their zone"""
    manager = request.user.profile
    
    if request.method == 'POST':
        category_id = request.POST.get('category')
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        unit = request.POST.get('unit')
        stock = request.POST.get('stock')
        image = request.FILES.get('image')
        
        try:
            category = Category.objects.get(id=category_id)
            
            Product.objects.create(
                category=category,
                zone=manager.zone_assigned,
                title=title,
                description=description,
                price=price,
                unit=unit,
                stock=stock,
                image=image
            )
            messages.success(request, f'পণ্য "{title}" যোগ করা হয়েছে।')
            return redirect('manager_products')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    categories = Category.objects.all()
    
    context = {
        'categories': categories,
        'manager': manager,
        'unit_choices': Product.UNIT_CHOICES,
    }
    return render(request, 'shop/manager/product_form.html', context)


@login_required(login_url='login')
@user_passes_test(is_manager)
def manager_product_edit(request, prod_id):
    """Manager edits product in their zone"""
    manager = request.user.profile
    product = get_object_or_404(Product, id=prod_id, zone=manager.zone_assigned)
    
    if request.method == 'POST':
        product.category_id = request.POST.get('category')
        product.title = request.POST.get('title')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        product.unit = request.POST.get('unit')
        product.stock = request.POST.get('stock')
        product.is_available = request.POST.get('is_available') == 'on'
        
        if request.FILES.get('image'):
            product.image = request.FILES.get('image')
        
        product.save()
        messages.success(request, f'পণ্য "{product.title}" আপডেট হয়েছে।')
        return redirect('manager_products')
    
    categories = Category.objects.all()
    
    context = {
        'product': product,
        'categories': categories,
        'manager': manager,
        'unit_choices': Product.UNIT_CHOICES,
    }
    return render(request, 'shop/manager/product_form.html', context)


@login_required(login_url='login')
@user_passes_test(is_manager)
def manager_product_delete(request, prod_id):
    """Manager deletes product from their zone"""
    manager = request.user.profile
    product = get_object_or_404(Product, id=prod_id, zone=manager.zone_assigned)
    title = product.title
    product.delete()
    messages.success(request, f'পণ্য "{title}" ডিলিট করা হয়েছে।')
    return redirect('manager_products')


# ================ MANAGER CATEGORIES ================
@login_required(login_url='login')
@user_passes_test(is_manager)
def manager_categories(request):
    """Manager can view all categories"""
    categories = Category.objects.all()
    
    context = {
        'categories': categories,
    }
    return render(request, 'shop/manager/categories.html', context)


@login_required(login_url='login')
@user_passes_test(is_manager)
def manager_category_add(request):
    """Manager adds new category"""
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        
        if Category.objects.filter(name=name).exists():
            messages.error(request, 'এই নাম ইতিমধ্যে ব্যবহৃত হয়েছে।')
        else:
            from django.utils.text import slugify
            slug = slugify(name)
            Category.objects.create(
                name=name,
                slug=slug,
                description=description,
                image=image
            )
            messages.success(request, f'ক্যাটেগরি "{name}" যোগ করা হয়েছে।')
            return redirect('manager_categories')
    
    return render(request, 'shop/manager/category_form.html')


@login_required(login_url='login')
@user_passes_test(is_manager)
def manager_category_edit(request, cat_id):
    """Manager edits category"""
    category = get_object_or_404(Category, id=cat_id)
    
    if request.method == 'POST':
        category.name = request.POST.get('name')
        category.description = request.POST.get('description')
        if request.FILES.get('image'):
            category.image = request.FILES.get('image')
        category.save()
        
        messages.success(request, f'ক্যাটেগরি "{category.name}" আপডেট হয়েছে।')
        return redirect('manager_categories')
    
    context = {'category': category}
    return render(request, 'shop/manager/category_form.html', context)


@login_required(login_url='login')
@user_passes_test(is_manager)
def manager_category_delete(request, cat_id):
    """Manager deletes category"""
    category = get_object_or_404(Category, id=cat_id)
    name = category.name
    category.delete()
    messages.success(request, f'ক্যাটেগরি "{name}" ডিলিট করা হয়েছে।')
    return redirect('manager_categories')


# ================ HERO SLIDES ================
@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_hero_slides(request):
    """Admin can manage hero slides"""
    slides = HeroSlide.objects.all()
    
    context = {
        'slides': slides,
    }
    return render(request, 'shop/admin/hero_slides.html', context)


@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_hero_slide_add(request):
    """Admin adds new hero slide"""
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        button_text = request.POST.get('button_text', 'Order Now')
        button_link = request.POST.get('button_link', '/register/')
        image = request.FILES.get('background_image')
        is_active = request.POST.get('is_active') == 'on'
        order = request.POST.get('order', 0)
        
        try:
            HeroSlide.objects.create(
                title=title,
                description=description,
                button_text=button_text,
                button_link=button_link,
                background_image=image,
                is_active=is_active,
                order=int(order)
            )
            messages.success(request, 'Hero slide added successfully!')
            return redirect('admin_hero_slides')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    return render(request, 'shop/admin/hero_slide_form.html')


@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_hero_slide_edit(request, slide_id):
    """Admin edits hero slide"""
    slide = get_object_or_404(HeroSlide, id=slide_id)
    
    if request.method == 'POST':
        slide.title = request.POST.get('title')
        slide.description = request.POST.get('description')
        slide.button_text = request.POST.get('button_text', 'Order Now')
        slide.button_link = request.POST.get('button_link', '/register/')
        slide.is_active = request.POST.get('is_active') == 'on'
        slide.order = int(request.POST.get('order', 0))
        
        if request.FILES.get('background_image'):
            slide.background_image = request.FILES.get('background_image')
        
        slide.save()
        messages.success(request, 'Hero slide updated successfully!')
        return redirect('admin_hero_slides')
    
    context = {'slide': slide}
    return render(request, 'shop/admin/hero_slide_form.html', context)


@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_hero_slide_delete(request, slide_id):
    """Admin deletes hero slide"""
    slide = get_object_or_404(HeroSlide, id=slide_id)
    title = slide.title
    slide.delete()
    messages.success(request, f'Hero slide "{title}" deleted successfully!')
    return redirect('admin_hero_slides')
