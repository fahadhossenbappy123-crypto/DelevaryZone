# Google Maps API - Quick Setup Guide

## 🔑 API Key পেতে ৫ মিনিটে

### Step 1: Google Cloud Console এ যান
```
URL: https://console.cloud.google.com
```

### Step 2: নতুন Project তৈরি করুন
```
1. "Select a Project" ক্লিক করুন (টপ left)
2. "NEW PROJECT" ক্লিক করুন
3. Name: "ZoneDelivery"
4. CREATE ক্লিক করুন
5. অপেক্ষা করুন ২-৩ সেকেন্ড
```

### Step 3: APIs Enable করুন
```
1. Search bar এ "Maps JavaScript API" লিখুন
2. এটি click করুন
3. "ENABLE" বাটন ক্লিক করুন

4. স্যাম উপায়ে এগুলো enable করুন:
   - Places API (Address autocomplete এর জন্য)
   - Geocoding API (Address ↔ Coordinates)
   - Directions API (Navigation এর জন্য)
```

### Step 4: API Key তৈরি করুন
```
1. Left sidebar এ "Credentials" ক্লিক করুন
2. "CREATE CREDENTIALS" → "API Key"
3. Key এর নাম দেখাবে (copy করুন)
4. "RESTRICT KEY" ক্লিক করুন
```

### Step 5: Restrictions যোগ করুন
```
1. Application restrictions:
   - "HTTP referrers (web sites)" নির্বাচন করুন
   - Add referrer: http://localhost:8000/*
   - Add referrer: আপনার production domain

2. API restrictions:
   - "Restrict key" নির্বাচন করুন
   - Select APIs:
     ✓ Maps JavaScript API
     ✓ Places API
     ✓ Geocoding API
     ✓ Directions API

3. SAVE করুন
```

---

## 💾 Django তে সেট করুন

### Option 1: settings.py এ সরাসরি (Development)
```python
# zonedelivery/settings.py
GOOGLE_MAPS_API_KEY = 'AIzaSyD...'  # আপনার key এখানে
```

### Option 2: Environment Variable (Recommended)

**Windows:**
```powershell
# একবারের জন্য
$env:GOOGLE_MAPS_API_KEY = "আপনার_API_KEY"

# Permanent (System Properties এ যান)
[System.Environment]::SetEnvironmentVariable("GOOGLE_MAPS_API_KEY", "আপনার_API_KEY", "User")
```

**Linux/Mac:**
```bash
export GOOGLE_MAPS_API_KEY="আপনার_API_KEY"

# Permanent (in .bashrc or .zshrc)
echo 'export GOOGLE_MAPS_API_KEY="আপনার_API_KEY"' >> ~/.bashrc
```

**Django তে access করতে:**
```python
import os
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', 'YOUR_KEY_HERE')
```

---

## ✅ Testing করুন

```python
# Django shell খুলুন
python manage.py shell

# এটি run করুন
from django.conf import settings
from shop.utils import get_google_maps_api_key

api_key = get_google_maps_api_key()
print(f"API Key configured: {bool(api_key)}")
print(f"Key: {api_key}")
```

---

## 🗺️ Checkout এ Google Maps যুক্ত করুন

### Step 1: Checkout Form Updated
সেtings এ API key configure করলে checkout template automatically access করতে পারবে।

### Step 2: JavaScript এ Google Maps
```html
<!-- checkout.html এ যুক্ত করুন -->
<script src="https://maps.googleapis.com/maps/api/js?key={{ google_maps_api_key }}&libraries=places"></script>

<script>
// Address autocomplete
let autocomplete;
const addressInput = document.getElementById('delivery_address');

autocomplete = new google.maps.places.Autocomplete(addressInput);
autocomplete.addListener('place_changed', function() {
    const place = autocomplete.getPlace();
    
    if (place.geometry) {
        document.getElementById('latitude').value = place.geometry.location.lat();
        document.getElementById('longitude').value = place.geometry.location.lng();
    }
});
</script>
```

---

## 🚀 Production Deployment

### Billing সেট করুন
```
1. Google Cloud Console এ যান
2. Billing → Link Billing Account (নতুন account তৈরি করুন যদি প্রয়োজন)
3. Free tier limit: $200/month automated credit
4. যতক্ষণ free credit থাকে, charge হবে না
```

### API Request Limits
```
Maps JavaScript API:
- ৩০,০০০ requests/day (first 25,000 free)
- Usage-based pricing: $7 per 1000 requests

Places API:
- Autocomplete: $0.017 per request
- Details lookup: $0.017 per request

Set daily usage limits in quota section
```

### Environment Security
```python
# .env file তৈরি করুন
GOOGLE_MAPS_API_KEY=আপনার_API_KEY
DJANGO_SECRET_KEY=...
DEBUG=False
```

```python
# settings.py এ
from decouple import config
GOOGLE_MAPS_API_KEY = config('GOOGLE_MAPS_API_KEY')
```

---

## 🐛 Common Issues ও সমাধান

### Issue 1: API Key Invalid
```
Error: "The provided API key is invalid"
Solution: 
1. Key কপি-পেস্ট করুন সঠিকভাবে
2. Key এ কোনো extra space নেই কিনা চেক করুন
3. Restrictions check করুন
```

### Issue 2: Google Maps loading নেই
```
Error: Maps না দেখা যাচ্ছে
Solution:
1. settings.py তে API_KEY configure আছে কিনা চেক করুন
2. Browser console এ error check করুন (F12)
3. API enable আছে কিনা verify করুন
```

### Issue 3: CORS Error
```
Error: "Access denied" CORS issue
Solution:
1. HTTP referrer restriction যুক্ত করুন
2. localhost:8000 যুক্ত করুন development এ
```

### Issue 4: Quota Exceeded
```
Error: Daily quota exceeded
Solution:
1. Billing account setup করুন
2. Usage limits increase করুন quota section এ
3. API caching implement করুন
```

---

## 📊 Quota ম্যানেজমেন্ট

### Daily Quota Check
```
1. APIs & Services → Quotas
2. Maps JavaScript API select করুন
3. Daily usage দেখুন
4. Quota update করুন প্রয়োজন অনুযায়ী
```

### Cost Optimization
```
1. Browser caching ব্যবহার করুন
2. Request batching করুন
3. Unnecessary requests avoid করুন
4. CDN ব্যবহার করুন (CloudFlare)
```

---

## 📝 Template Example

```html
<!-- Address Autocomplete Field -->
<input type="text" 
       id="delivery_address" 
       name="delivery_address" 
       class="form-control" 
       placeholder="শুরু করুন এড্রেস লিখতে...">

<!-- Hidden fields for coordinates -->
<input type="hidden" id="latitude" name="latitude">
<input type="hidden" id="longitude" name="longitude">

<!-- Map Container -->
<div id="checkout_map" style="width: 100%; height: 400px;"></div>

<script src="https://maps.googleapis.com/maps/api/js?key={{google_maps_api_key}}&libraries=places"></script>
<script>
let map;
let marker;

function initMap() {
    map = new google.maps.Map(document.getElementById('checkout_map'), {
        zoom: 15,
        center: {lat: 23.8103, lng: 90.4125}  // Dhaka default
    });
    
    marker = new google.maps.Marker({map: map});
}

// Autocomplete
const autocomplete = new google.maps.places.Autocomplete(
    document.getElementById('delivery_address')
);

autocomplete.addListener('place_changed', function() {
    const place = autocomplete.getPlace();
    if (place.geometry) {
        map.setCenter(place.geometry.location);
        marker.setPosition(place.geometry.location);
        
        document.getElementById('latitude').value = place.geometry.location.lat();
        document.getElementById('longitude').value = place.geometry.location.lng();
    }
});

initMap();
</script>
```

---

## ✅ Checklist

- [ ] Google Cloud Account তৈরি করেছেন?
- [ ] New Project তৈরি করেছেন?
- [ ] Maps JavaScript API enable করেছেন?
- [ ] Places API enable করেছেন?
- [ ] API Key তৈরি করেছেন?
- [ ] HTTP referrers restriction যুক্ত করেছেন?
- [ ] Django settings.py তে key configure করেছেন?
- [ ] Checkout template update করেছেন?
- [ ] Testing করেছেন?
- [ ] Production deployment ready?

---

**Next:** Checkout template এ Google Maps integrate করার জন্য আরও কোড samples পেতে পারেন।
