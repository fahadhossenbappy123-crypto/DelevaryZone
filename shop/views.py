from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import models
from django.http import JsonResponse
from .models import Category, Product, UserProfile, Zone, Order, OrderItem, Notification
from .forms import UserRegisterForm, UserLoginForm, UserProfileForm, CheckoutForm
from .utils import (
    calculate_distance, 
    check_location_in_zones,
    get_delivery_charge_for_zone,
    get_google_maps_api_key
)
import json
import uuid


def home(request):
    zones = Zone.objects.filter(is_active=True)
    selected_zone = request.GET.get('zone')
    
    if selected_zone:
        products = Product.objects.filter(zone_id=selected_zone, is_available=True)[:12]
    else:
        products = Product.objects.filter(is_available=True)[:12]
    
    categories = Category.objects.all()
    
    context = {
        'categories': categories,
        'products': products,
        'zones': zones,
        'selected_zone': selected_zone,
        'title': 'ZoneDelivery - তোমার জোনের ডেলিভারি'
    }
    return render(request, 'shop/home.html', context)


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user, role='customer')
            messages.success(request, 'অ্যাকাউন্ট সফলভাবে তৈরি হয়েছে! এখন লগইন করুন।')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = UserRegisterForm()
    
    return render(request, 'shop/register.html', {'form': form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'স্বাগতম {user.username}!')
                return redirect('home')
            else:
                messages.error(request, 'ইউজারনেম বা পাসওয়ার্ড ভুল।')
    else:
        form = UserLoginForm()
    
    return render(request, 'shop/login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.success(request, 'লগআউট করেছেন সফলভাবে।')
    return redirect('home')


@login_required(login_url='login')
def profile(request):
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user, role='customer')
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            request.user.first_name = form.cleaned_data.get('first_name', '')
            request.user.last_name = form.cleaned_data.get('last_name', '')
            request.user.email = form.cleaned_data.get('email', '')
            request.user.save()
            profile.save()
            messages.success(request, 'প্রোফাইল আপডেট হয়েছে সফলভাবে।')
            return redirect('profile')
    else:
        initial_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }
        form = UserProfileForm(instance=profile, initial=initial_data)
    
    context = {
        'profile': profile,
        'form': form,
    }
    return render(request, 'shop/profile.html', context)


@login_required(login_url='login')
def my_orders(request):
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')
    
    context = {
        'orders': orders,
    }
    return render(request, 'shop/my_orders.html', context)


@login_required(login_url='login')
def order_detail(request, order_id):
    try:
        order = Order.objects.get(order_id=order_id, customer=request.user)
    except Order.DoesNotExist:
        messages.error(request, 'অর্ডার পাওয়া যায়নি।')
        return redirect('my_orders')
    
    items = order.items.all()
    total_price = order.total_amount + order.delivery_charge
    
    context = {
        'order': order,
        'items': items,
        'total_price': total_price,
    }
    return render(request, 'shop/order_detail.html', context)


def rider_dashboard(request):
    """রাইডারদের জন্য Management Panel"""
    from django.utils import timezone
    
    # Rider check
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'rider':
        messages.error(request, 'আপনি রাইডার নন।')
        return redirect('home')
    
    # Handle POST requests (order accept/status update)
    if request.method == 'POST':
        action = request.POST.get('action')
        order_id = request.POST.get('order_id')
        
        try:
            if action == 'accept':
                # Rider accepts an order
                order = Order.objects.get(id=order_id)
                if order.rider is None:
                    order.rider = request.user
                    order.status = 'confirmed'
                    order.save()
                    messages.success(request, f'অর্ডার #{order.order_id} গ্রহণ করা হয়েছে।')
                else:
                    messages.error(request, 'এই অর্ডার ইতিমধ্যে নিয়োগ করা হয়েছে।')
            
            elif action == 'update_status':
                # Update order status
                order = Order.objects.get(id=order_id)
                if order.rider == request.user:
                    status = request.POST.get('status')
                    order.status = status
                    order.save()
                    
                    status_text = 'পিক আপ' if status == 'picked' else 'ডেলিভারি সম্পন্ন'
                    messages.success(request, f'অর্ডার #{order.order_id} {status_text} চিহ্নিত করা হয়েছে।')
                else:
                    messages.error(request, 'অনুমতি নেই।')
        except Order.DoesNotExist:
            messages.error(request, 'অর্ডার পাওয়া যায়নি।')
    
    # Get data for dashboard
    # Pending orders (no rider assigned yet, confirmed status)
    pending_orders = Order.objects.filter(
        status='pending', 
        rider__isnull=True
    ).select_related('customer', 'zone')
    
    # Active deliveries for this rider (confirmed or picked)
    active_deliveries = Order.objects.filter(
        rider=request.user,
        status__in=['confirmed', 'picked']
    ).select_related('customer', 'zone').prefetch_related('items')
    
    # Completed deliveries
    completed_orders = Order.objects.filter(
        rider=request.user,
        status='delivered'
    ).select_related('customer', 'zone').order_by('-created_at')
    
    # Stats
    completed_count = completed_orders.count()
    total_earnings = completed_orders.aggregate(
        total=models.Sum('delivery_charge')
    )['total'] or 0
    
    context = {
        'pending_orders': pending_orders,
        'active_deliveries': active_deliveries,
        'completed_orders': completed_orders,
        'completed_count': completed_count,
        'total_earnings': total_earnings,
        'today': timezone.now(),
    }
    return render(request, 'shop/rider_dashboard.html', context)


# ============ RIDER ORDER DETAIL ============
@login_required(login_url='login')
def rider_order_detail(request, order_id):
    """Rider can view order details with customer location map"""
    # Check if user is a rider
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'rider':
        messages.error(request, 'আপনি রাইডার নন।')
        return redirect('home')
    
    # Get the order
    order = get_object_or_404(Order, id=order_id)
    
    # Check if rider has access to this order
    if order.rider != request.user:
        messages.error(request, 'আপনার কাছে এই অর্ডার দেখার অনুমতি নেই।')
        return redirect('rider_dashboard')
    
    # Get order items
    items = order.items.all()
    
    # Handle status update
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in dict(Order._meta.get_field('status').choices):
            order.status = status
            order.save()
            status_text = 'পিক আপ' if status == 'picked' else 'ডেলিভারি সম্পন্ন'
            messages.success(request, f'অর্ডার #{order.order_id} {status_text} চিহ্নিত করা হয়েছে।')
            return redirect('rider_order_detail', order_id=order.id)
    
    context = {
        'order': order,
        'items': items,
        'status_choices': Order._meta.get_field('status').choices,
    }
    return render(request, 'shop/rider_order_detail.html', context)


# ============ MAP & GEOLOCATION ============
def user_map(request):
    """User-facing map with live location and zone check"""
    zones = Zone.objects.filter(is_active=True)
    
    context = {
        'zones': zones,
        'title': 'Service Zone Map - Live Location'
    }
    return render(request, 'shop/user_map.html', context)


def api_zones(request):
    """API endpoint to get all zones data (lat, lng, radius)"""
    zones = Zone.objects.filter(is_active=True)
    
    zones_data = []
    for zone in zones:
        if zone.latitude and zone.longitude:
            zones_data.append({
                'id': zone.id,
                'name': zone.name,
                'latitude': zone.latitude,
                'longitude': zone.longitude,
                'radius': zone.radius,
                'description': zone.description,
                'delivery_charge': str(zone.delivery_charge),
            })
    
    return JsonResponse({'zones': zones_data})


def api_check_location(request):
    """Check if user's location is within any service zone"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        user_lat = float(data.get('latitude'))
        user_lon = float(data.get('longitude'))
    except (json.JSONDecodeError, ValueError, TypeError):
        return JsonResponse({'error': 'Invalid coordinates'}, status=400)
    
    # Use utility function
    result = check_location_in_zones(user_lat, user_lon)
    
    return JsonResponse({
        'user_location': {
            'latitude': user_lat,
            'longitude': user_lon,
        },
        'is_in_service': result['is_in_service'],
        'zones': result['service_zones'],
    })


# ============ SHOPPING CART ============
def get_cart(request):
    """Get cart from session"""
    if 'cart' not in request.session:
        request.session['cart'] = {}
    return request.session['cart']


def set_cart(request, cart):
    """Save cart to session"""
    request.session['cart'] = cart
    request.session.modified = True


def add_to_cart(request, product_id):
    """Add product to cart"""
    try:
        product = Product.objects.get(id=product_id, is_available=True)
    except Product.DoesNotExist:
        messages.error(request, 'পণ্যটি পাওয়া যায়নি।')
        return redirect('home')
    
    cart = get_cart(request)
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        cart[product_id_str]['quantity'] += 1
    else:
        cart[product_id_str] = {
            'id': product.id,
            'title': product.title,
            'price': float(product.price),
            'image': product.image.url if product.image else '/static/placeholder.png',
            'quantity': 1,
            'zone_id': product.zone_id,
            'zone_name': product.zone.name if product.zone else 'N/A'
        }
    
    set_cart(request, cart)
    messages.success(request, f'"{product.title}" কার্টে যোগ করা হয়েছে।')
    
    # Return to previous page or home
    return redirect(request.META.get('HTTP_REFERER', 'home'))


def view_cart(request):
    """Display cart items"""
    cart = get_cart(request)
    
    cart_items = []
    total_price = 0
    total_quantity = 0
    
    for product_id_str, item in cart.items():
        item_total = item['price'] * item['quantity']
        total_price += item_total
        total_quantity += item['quantity']
        
        item['total'] = item_total
        cart_items.append(item)
    
    zones = Zone.objects.filter(is_active=True)
    
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_quantity': total_quantity,
        'zones': zones,
        'cart_empty': len(cart_items) == 0
    }
    
    return render(request, 'shop/cart.html', context)


def remove_from_cart(request, product_id):
    """Remove product from cart"""
    cart = get_cart(request)
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        product_title = cart[product_id_str]['title']
        del cart[product_id_str]
        set_cart(request, cart)
        messages.success(request, f'"{product_title}" কার্ট থেকে সরানো হয়েছে।')
    
    return redirect('view_cart')


def update_cart_quantity(request, product_id):
    """Update product quantity in cart"""
    if request.method == 'POST':
        quantity = request.POST.get('quantity', 1)
        cart = get_cart(request)
        product_id_str = str(product_id)
        
        try:
            quantity = int(quantity)
            if quantity > 0:
                if product_id_str in cart:
                    cart[product_id_str]['quantity'] = quantity
                    set_cart(request, cart)
                    messages.success(request, 'কার্ট আপডেট হয়েছে।')
            else:
                messages.error(request, 'পরিমাণ শূন্যের চেয়ে বেশি হতে হবে।')
        except ValueError:
            messages.error(request, 'অবৈধ পরিমাণ।')
    
    return redirect('view_cart')


def checkout(request):
    """Checkout page and order creation"""
    cart = get_cart(request)
    
    # Check if cart is empty
    if not cart:
        messages.error(request, 'আপনার কার্ট খালি আছে।')
        return redirect('view_cart')
    
    # Calculate totals
    cart_items = []
    total_price = 0
    
    for product_id_str, item in cart.items():
        item_total = item['price'] * item['quantity']
        total_price += item_total
        cart_items.append(item)
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Create order
            try:
                zone = form.cleaned_data['zone']
                
                # Get location from POST
                latitude = request.POST.get('latitude')
                longitude = request.POST.get('longitude')
                
                # Convert to float if provided
                try:
                    latitude = float(latitude) if latitude else None
                    longitude = float(longitude) if longitude else None
                except ValueError:
                    latitude = None
                    longitude = None
                
                # Generate unique order ID
                order_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"
                
                # Create order
                order = Order.objects.create(
                    order_id=order_id,
                    customer=request.user if request.user.is_authenticated else None,
                    zone=zone,
                    customer_phone=form.cleaned_data['phone'],
                    customer_email=form.cleaned_data['email'],
                    customer_address=form.cleaned_data['delivery_address'],
                    customer_city='',  # No city field in checkout
                    latitude=latitude,
                    longitude=longitude,
                    total_amount=total_price,
                    delivery_charge=zone.delivery_charge,
                    payment_method='cash',  # COD only
                    status='pending'
                )
                
                # Add items to order
                for product_id_str, item in cart.items():
                    try:
                        product = Product.objects.get(id=int(product_id_str))
                        OrderItem.objects.create(
                            order=order,
                            product=product,
                            quantity=item['quantity'],
                            price=item['price']
                        )
                    except Product.DoesNotExist:
                        pass
                
                # Clear cart
                request.session['cart'] = {}
                request.session.modified = True
                
                messages.success(request, f'আপনার অর্ডার {order_id} সফলভাবে তৈরি হয়েছে!')
                
                # Create notification for customer
                if request.user.is_authenticated:
                    create_notification(
                        user=request.user,
                        notification_type='order_confirmation',
                        title='Order Confirmed',
                        message=f'Your order #{order_id} has been placed successfully.',
                        order=order
                    )
                
                # Redirect to order detail if user logged in
                if request.user.is_authenticated:
                    return redirect('order_detail', order_id=order_id)
                else:
                    # For guest users, just show a success message
                    return render(request, 'shop/order_success.html', {
                        'order_id': order_id,
                        'total_amount': total_price + zone.delivery_charge,
                        'zone_name': zone.name
                    })
            
            except Exception as e:
                messages.error(request, f'অর্ডার তৈরিতে সমস্যা: {str(e)}')
    else:
        # Pre-fill form if user is logged in
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'full_name': f"{request.user.first_name or ''} {request.user.last_name or ''}".strip() or request.user.username,
                'email': request.user.email,
                'phone': request.user.profile.phone if hasattr(request.user, 'profile') else '',
                'delivery_address': request.user.profile.address if hasattr(request.user, 'profile') else '',
            }
        
        form = CheckoutForm(initial=initial_data)
    
    # Calculate total with delivery charge
    zones = Zone.objects.filter(is_active=True)
    default_delivery = zones.first().delivery_charge if zones else 50
    
    # Get Google Maps API Key
    api_key = get_google_maps_api_key()
    
    # Prepare zone data for JavaScript validation
    import json
    zones_data = []
    for zone in zones:
        zones_data.append({
            'id': zone.id,
            'name': zone.name,
            'latitude': zone.latitude,
            'longitude': zone.longitude,
            'radius': zone.radius,
            'delivery_charge': float(zone.delivery_charge)
        })
    zones_json = json.dumps(zones_data)
    
    context = {
        'form': form,
        'cart_items': cart_items,
        'total_price': total_price,
        'zones': zones,
        'zones_json': zones_json,
        'default_delivery': default_delivery,
        'google_maps_api_key': api_key,
    }
    
    return render(request, 'shop/checkout.html', context)


# ============ NOTIFICATION VIEWS ============

@login_required
def get_notifications(request):
    """Get all notifications for logged-in user with unread count"""
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:10]
    unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
    
    notifications_data = []
    for notif in notifications:
        notifications_data.append({
            'id': notif.id,
            'title': notif.title,
            'message': notif.message,
            'type': notif.notification_type,
            'is_read': notif.is_read,
            'order_id': notif.order.order_id if notif.order else None,
            'created_at': notif.created_at.strftime('%Y-%m-%d %H:%M'),
        })
    
    return JsonResponse({
        'notifications': notifications_data,
        'unread_count': unread_count,
    })


@login_required
def mark_notification_read(request, notif_id):
    """Mark a single notification as read"""
    notification = get_object_or_404(Notification, id=notif_id, user=request.user)
    notification.is_read = True
    notification.save()
    
    return JsonResponse({'status': 'success'})


@login_required
def mark_all_notifications_read(request):
    """Mark all notifications as read"""
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    
    return JsonResponse({'status': 'success'})


def create_notification(user, notification_type, title, message, order=None):
    """
    Helper function to create notifications
    Called from other views when order status changes
    """
    Notification.objects.create(
        user=user,
        notification_type=notification_type,
        title=title,
        message=message,
        order=order,
        is_read=False,
    )



