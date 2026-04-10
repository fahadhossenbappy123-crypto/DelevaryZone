# ZoneDelivery - Django E-Commerce Platform

একটি বাংলাদেশী ই-কমার্স প্ল্যাটফর্ম যা খাবার এবং পণ্য ডেলিভারি প্রদান করে।

## প্রোজেক্ট সেটআপ ✅

সব সেটআপ সম্পূর্ণ এবং চালু করার জন্য প্রস্তুত!

### দ্রুত স্টার্ট গাইড

**1. Virtual Environment চালু করুন:**
```bash
.\.venv\Scripts\activate.ps1
```

**2. সার্ভার চালু করুন:**
```bash
python manage.py runserver
```

**3. ব্রাউজারে খুলুন:**
- মূল সাইট: http://localhost:8000/
- Admin প্যানেল: http://localhost:8000/admin/

### Admin লগইন বিবরণ
- ইউজারনেম: `admin`
- পাসওয়ার্ড: `admin123`

---

## ফাংশনালিটি ✨

### বর্তমানে কী কাজ করছে:
- ✅ হোম পেজ (Categories & Products Display)
- ✅ Django Admin প্যানেল
- ✅ Category এবং Product ম্যানেজমেন্ট
- ✅ রেসপন্সিভ Bootstrap5 UI
- ✅ বাংলা ভাষা সাপোর্ট
- ✅ ইমেজ আপলোড সুবিধা

### ভবিষ্যতের বৈশিষ্ট্য:
- 🔄 Shopping Cart
- 👤 User Authentication/Profile
- 📦 Order Management
- 💳 Payment Integration
- 🗺️ Real-time Location Tracking

---

## কমান্ড রেফারেন্স

### ডেটাবেস
```bash
# নতুন মাইগ্রেশন তৈরি করুন
python manage.py makemigrations

# মাইগ্রেশন প্রয়োগ করুন
python manage.py migrate
```

### Admin
```bash
# নতুন সুপারইউজার তৈরি করুন
python manage.py createsuperuser
```

### সার্ভার
```bash
# ডেভেলপমেন্ট সার্ভার চালু করুন
python manage.py runserver 0.0.0.0:8000

# সার্ভার বন্ধ করুন
# Ctrl + Break (Windows)
```

---

## প্রোজেক্ট স্ট্রাকচার

```
ZoneDelivery/
├── manage.py                 # Django ম্যানেজমেন্ট
├── requirements.txt          # প্যাকেজ ডিপেন্ডেন্সিস
├── db.sqlite3               # ডেটাবেস (স্বয়ংক্রিয় তৈরি)
│
├── zonedelivery/            # প্রোজেক্ট কনফিগ
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── shop/                    # মেইন অ্যাপ
│   ├── models.py           # Category, Product
│   ├── views.py            # Home ভিউ
│   ├── urls.py
│   ├── admin.py            # Admin কনফিগ
│   ├── forms.py            # ফর্ম (ভবিষ্যতের জন্য)
│   └── templates/shop/
│       ├── base.html       # বেস টেমপ্লেট
│       ├── home.html       # হোম পেজ
│       └── category_list.html
│
└── media/                  # আপলোড করা ছবি
    ├── category/
    └── products/
```

---

## ডেটাবেস মডেল

### Category
- `name` - ক্যাটেগরির নাম (অনন্য)
- `slug` - URL-বন্ধুত্বপূর্ণ নাম
- `image` - ক্যাটেগরি ছবি
- `created_at` - তৈরির তারিখ

### Product
- `category` - কোন ক্যাটেগরিতে অন্তর্ভুক্ত
- `title` - পণ্যের নাম
- `description` - বিস্তারিত বর্ণনা
- `price` - মূল্য (টাকায়)
- `image` - পণ্য ছবি
- `stock` - স্টক পরিমাণ
- `is_available` - পাওয়া যায় কিনা
- `created_at` - তৈরির তারিখ

---

## Tech Stack 🛠️

- **Backend**: Django 5.1.7
- **Database**: SQLite3
- **Frontend**: Bootstrap 5
- **Image Handling**: Pillow
- **Static Files**: WhiteNoise

---

## টাইমজোন ও ভাষা

- **ভাষা**: বাংলা (Bengali)
- **টাইমজোন**: এশিয়া/ঢাকা

---

## ট্রাবলশুটিং ⚙️

**সার্ভার চালু হচ্ছে না?**
- Virtual Environment সক্রিয় আছে কিনা চেক করুন

### 🔴 Geolocation / Location Access কাজ করছে না

**সমস্যা**: Phone থেকে সাইট খোলে মেনে টপপার location access নেই

**কারণ**: Geolocation API এর জন্য **HTTPS প্রয়োজন**

#### সমাধান:

**Option 1: Localhost থেকে পরীক্ষা করুন (সবচেয়ে সহজ)**
```bash
# PC এ সার্ভার চালু করুন
python manage.py runserver

# PC এ ব্রাউজার খুলুন
http://localhost:8000
# ✅ কাজ করবে - Geolocation exception আছে
```

**Option 2: Phone থেকে পরীক্ষা করতে হলে HTTPS প্রয়োজন**
- Development এ Self-signed certificate তৈরি করুন:
```bash
# SSL Certificate তৈরি করুন (Windows)
# এটি Windows এ PowerShell এ চালান:
$cert = New-SelfSignedCertificate -DnsName localhost -CertStoreLocation Cert:\CurrentUser\My
```

**Option 3: Ngrok দিয়ে Production-like HTTPS tunnel**
```bash
# Ngrok ইনস্টল: https://ngrok.com
ngrok http 8000

# এর পর নতুন HTTPS URL পাবেন:
# https://xxxxx.ngrok.io → এটি phone এ ব্যবহার করুন
```

**Option 4: Phone সেটিংস চেক**
- ✅ Phone এ Location Service চালু?
  - Settings → Location → ON
- ✅ Browser এ Permission দেওয়া?
  - Chrome Settings → Privacy → Site Settings → Location
  - Site পারমিশন → Allow

**দ্রুত চেক:**
- PC: `http://localhost:8000` → ✅ Geolocation কাজ করবে
- Phone from same network: `http://192.168.x.x:8000` → ❌ Geolocation ব্লক (HTTPS প্রয়োজন)
- `pip install -r requirements.txt` দিয়ে প্যাকেজ ইনস্টল করুন

**পোর্ট ব্যবহৃত?**
```bash
python manage.py runserver 8001
```

**ডাটাবেস সমস্যা?**
```bash
python manage.py migrate
```

---

## লাইসেন্স 📄

এই প্রোজেক্ট শিক্ষা এবং ব্যক্তিগত ব্যবহারের জন্য।

---

**প্রস্তুত! এখন শুরু করুন: `python manage.py runserver`** 🚀
