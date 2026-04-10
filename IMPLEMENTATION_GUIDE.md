# ZoneDelivery - Refactoring & Google Maps Implementation Guide

## 🎯 কী করা হয়েছে?

আপনার প্রজেক্ট সম্পূর্ণভাবে refactor করা হয়েছে এবং নতুন features যুক্ত করা হয়েছে। এখানে আপনার ওয়ার্কফ্লো অনুযায়ী সবকিছু সাজানো হয়েছে।

---

## 📊 নতুন সিস্টেম আর্কিটেকচার

### ১. **Customer Workflow** ✅
```
গ্রাহক হোম পেজে যায়
    ↓
কেটাগরি/পণ্য ব্রাউজ করে
    ↓
কার্টে যুক্ত করে
    ↓
Checkout পেজে যায় [এখানে GPS লোকেশন capture হবে]
    ↓
Order তৈরি হয় (Status: Pending) → Manager নোটিফিকেশন পায়
```

### ২. **Manager Workflow** 🆕 (যুক্ত করা হয়েছে)
```
ম্যানেজার ড্যাশবোর্ডে লগইন করে
    ↓
Pending অর্ডার দেখে
    ↓
অর্ডার বিবরণ দেখে + গ্রাহক মানি জানায়
    ↓
অর্ডার APPROVE/REJECT করে
    ↓
(Approve হলে) → রাইডার নির্ধারণ করে
    ↓
Order Status: Approved → Confirmed
```

### ३. **Rider Workflow** ✅
```
রাইডার ড্যাশবোর্ডে লগইন করে
    ↓
Confirmed অর্ডার দেখে
    ↓
গ্রাহক লোকেশন Google Maps এ দেখে [নতুন]
    ↓
"Picked" বাটন ক্লিক
    ↓
ডেলিভারি এ যায় 
    ↓
"Delivered" বাটন ক্লিক
    ↓
Order Status: Delivered ✅
```

### ४. **Admin Dashboard** ✅
```
সব Orders track করে
সব Riders track করে
সব Managers track করে
Reports দেখে
```

---

## 🔧 করা পরিবর্তন

### ✅ Models (shop/models.py)
```python
# UserProfile এ যুক্ত হয়েছে:
- role = 'manager' (নতুন ভূমিকা)
- zone_assigned (Manager যে Zone এর জওয়াব দেয়)

# Order model এ যুক্ত হয়েছে:
- manager (যে Manager approval দিয়েছে)
- manager_approval_reason (reject হলে কেন?)
- manager_responded_at (কখন respond করেছে)
- address_formatted (Google Maps address)
- status = 'approved' (নতুন status)
```

### ✅ Utility Functions (shop/utils.py)
```python
calculate_distance()          # হারভারসাইন ফর্মুলা
check_location_in_zones()     # জোন ভ্যালিডেশন
get_delivery_charge_for_zone() # ডেলিভারি চার্জ
get_google_maps_api_key()    # API key
validate_coordinates()        # ইনপুট ভ্যালিডেশন
is_delivery_possible()        # সম্পূর্ণ চেক
```

### ✅ Manager Panel Views (shop/admin_views.py)
- `manager_dashboard()` - সব অর্ডার দেখায়
- `manager_approve_order()` - অর্ডার approve/reject করতে
- `manager_assign_rider()` - রাইডার নির্ধারণ করতে

### ✅ Templates
```
shop/manager/dashboard.html      # Manager dashboard
shop/manager/approve_order.html   # Order approval পেজ
shop/manager/assign_rider.html    # Rider assignment
shop/templatetags/custom_filters.py # Django template filter
```

### ✅ URLs (shop/urls.py)
```python
path('manager/', manager_dashboard)
path('manager/order/<id>/approve/', manager_approve_order)
path('manager/order/<id>/assign-rider/', manager_assign_rider)
```

---

## 🔑 Google Maps API সেটআপ

### Step 1: API Key পেতে হবে
```bash
1. https://console.cloud.google.com খুলুন
2. নতুন Project তৈরি করুন
3. APIs enable করুন:
   - Maps JavaScript API
   - Places API (Address autocomplete এর জন্য)
   - Directions API (Navigation এর জন্য)
4. Credentials → API Key তৈরি করুন
5. HTTP referrers restriction যোগ করুন আপনার ডোমেইন
```

### Step 2: settings.py এ API Key যোগ করুন

**Option A: Direct (Development)**
```python
# settings.py
GOOGLE_MAPS_API_KEY = 'AIzaSyD...'  # আপনার key এখানে
```

**Option B: Environment Variable (Production - আরও নিরাপদ)**
```python
import os
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', 'YOUR_KEY_HERE')
```

Windows PowerShell তে:
```powershell
$env:GOOGLE_MAPS_API_KEY = 'আপনার_API_KEY'
```

---

## 🚀 কীভাবে ব্যবহার করবেন?

### Manager তৈরি করতে হবে

**Django Admin প্যানেলে:**
```
1. http://localhost:8000/admin খুলুন
2. Users বিভাগে নতুন user তৈরি করুন
3. User Profile এ গিয়ে:
   - Role: "ম্যানেজার"
   - Zone Assigned: একটি Zone নির্বাচন করুন
4. Save করুন
```

### Manager ড্যাশবোর্ড অ্যাক্সেস করতে হবে

```
1. Manager user দিয়ে লগইন করুন
2. Navigation bar এ "Manager Panel" বাটন দেখবেন
3. ক্লিক করলে Dashboard খুলবে
```

### অর্ডার Approve প্রসেস

```
1. "নতুন অর্ডার" ট্যাবে pending orders দেখবেন
2. একটি অর্ডারে ক্লিক করুন
3. অর্ডার বিবরণ দেখে "অনুমোদন করুন" ক্লিক করুন
4. অনুমোদিত ট্যাবে যাবে
```

### Rider নির্ধারণ প্রসেস

```
1. "অনুমোদিত" ট্যাবে অর্ডার দেখবেন
2. "রাইডার নির্ধারণ করুন" ক্লিক করুন
3. একজন রাইডার নির্বাচন করুন
4. Assign করুন
5. রাইডার তার ড্যাশবোর্ডে order দেখবে
```

---

## 📝 Database Migration

সব মডেল পরিবর্তন প্রয়োজনীয় migration তৈরি করা হয়েছে এবং applied হয়েছে:

```bash
# Migration file: shop/migrations/0006_order_address_formatted_order_manager_and_more.py

Changes:
+ Add field address_formatted to order
+ Add field manager to order
+ Add field manager_approval_reason to order
+ Add field manager_responded_at to order
+ Add field zone_assigned to userprofile
~ Alter field rider on order
~ Alter field status on order
~ Alter field role on userprofile
```

---

## ⏳ পরবর্তী Steps (Google Maps ইন্টিগ্রেশন)

### Phase 1: Checkout Map (অগ্রাধিকার ১)
- [ ] Checkout form এ Google Maps integrate করুন
- [ ] Address Autocomplete যুক্ত করুন
- [ ] Location picker implement করুন
- [ ] GPS + Manual address support

### Phase 2: Rider Map (অগ্রাধিকার ২)
- [ ] Rider order detail এ Google Maps দেখান
- [ ] Customer location কাছে Marker রাখুন
- [ ] Navigation button যুক্ত করুন
- [ ] Directions API ব্যবহার করুন

### Phase 3: Live Tracking (Optional)
- [ ] Real-time rider location tracking
- [ ] WebSocket অথবা Ajax polling
- [ ] Map এ live marker update

### Phase 4: Admin Enhancements
- [ ] Live dashboard এ সব riders দেখান
- [ ] Heat map of orders
- [ ] Performance reports

---

## 🔐 নিরাপত্তা টিপস

1. **API Key Protection**
   - Environment variables ব্যবহার করুন
   - `.env` file ব্যবহার করুন (`.gitignore` তে রাখুন)
   - HTTP referrer restrictions যুক্ত করুন

2. **CSRF Protection**
   - সব POST endpoints `@csrf_protect` decorator আছে
   - Forms এ `{% csrf_token %}` আছে

3. **Permission Checking**
   - সব manager views এ `@user_passes_test(is_manager)` আছে
   - Order access properly validated হয়েছে

---

## ⚙️ Configuration

### Required Settings
```python
# settings.py
GOOGLE_MAPS_API_KEY = 'YOUR_API_KEY_HERE'
LANGUAGE_CODE = 'bn'  # Bengali
TIME_ZONE = 'Asia/Dhaka'
```

### Optional Customization
```python
# Zone defaults
DEFAULT_ZONE_RADIUS = 2000  # meters
DELIVERY_CHARGE_DEFAULT = 50  # BDT

# Geolocation
USE_GEOLOCATION = True
REQUIRE_GEOLOCATION = False  # Checkout এ mandatory কিনা
```

---

## 🐛 Troubleshooting

### API Key সমস্যা
```python
# Check if API key is configured
from django.conf import settings
api_key = settings.GOOGLE_MAPS_API_KEY
print(api_key)  # ডিবাগিং এর জন্য
```

### Manager access নেই?
```
1. User admin panel এ যান
2. User Profile চেক করুন
3. role = 'manager' নিশ্চিত করুন
4. zone_assigned value আছে কিনা চেক করুন
```

### Order status সমস্যা
```python
# Database এ status check করুন
from shop.models import Order
Order.objects.values_list('status', flat=True).distinct()
```

---

## 📚 Reference

### File Structure
```
ZoneDelivery/
├── shop/
│   ├── models.py (✅ Updated)
│   ├── views.py (✅ Refactored)
│   ├── admin_views.py (✅ Manager views added)
│   ├── urls.py (✅ Manager URLs added)
│   ├── utils.py (✅ NEW - Helper functions)
│   ├── forms.py
│   ├── templates/
│   │   └── shop/
│   │       ├── manager/ (✅ NEW)
│   │       │   ├── dashboard.html
│   │       │   ├── approve_order.html
│   │       │   └── assign_rider.html
│   │       ├── base.html (✅ Updated navbar)
│   │       ├── checkout.html
│   │       └── ...
│   └── templatetags/ (✅ NEW)
│       ├── custom_filters.py
│       └── __init__.py
├── zonedelivery/
│   └── settings.py (✅ API key config added)
└── ...
```

---

## ✨ কী নতুন?

| Feature | Status | Description |
|---------|--------|-------------|
| Manager Role | ✅ | নতুন ভূমিকা - অর্ডার approval |
| Manager Dashboard | ✅ | সব pending orders দেখতে |
| Order Approval | ✅ | Manager approve/reject করতে পারবে |
| Rider Assignment | ✅ | Manager rider নির্ধারণ করতে পারবে |
| Utility Functions | ✅ | Helper functions separated |
| Google Maps Config | ✅ | settings.py তে configuration |
| Custom Template Tags | ✅ | mul filter যুক্ত করেছি |
| Enhanced Order Model | ✅ | Manager tracking fields |
| Navbar Updates | ✅ | Manager panel link যুক্ত |
| Database Migration | ✅ | Applied successfully |

---

## 🎓 শেখার পয়েন্ট

1. **Django Best Practices**
   - Separation of concerns (utils.py)
   - Permission-based access control
   - Template inheritance

2. **Google Maps Integration** (পরবর্তীতে)
   - JavaScript API ব্যবহার
   - Address autocomplete
   - Direction routing

3. **Real-time Updates** (Optional)
   - WebSocket কিভাবে ব্যবহার করতে হয়
   - Django Channels
   - Redis integration

---

## 📞 Support

যদি কোনো সমস্যা হয়, এই পয়েন্টগুলো চেক করুন:

1. ✅ Migrations applied হয়েছে কিনা?
2. ✅ Manager user create করেছেন কিনা?
3. ✅ zone_assigned value set করেছেন কিনা?
4. ✅ সব URL patterns add করেছেন কিনা?
5. ✅ Templates ঠিকঠাক render হচ্ছে কিনা?

---

**Last Updated:** April 2026  
**Version:** 1.0  
**Status:** ✅ Ready for Google Maps Integration
