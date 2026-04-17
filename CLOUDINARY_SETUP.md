# 🌥️ Cloudinary Setup Guide

## **কেন Cloudinary ব্যবহার করি?**

✅ **Free Tier**: 100GB storage (unlimited images)  
✅ **Easy Setup**: কোনো billing hassle নেই  
✅ **Image Optimization**: Auto quality & format optimization  
✅ **Video Support**: Images এবং videos দুটোই  
✅ **Global CDN**: Very fast delivery  
✅ **API**: Simple এবং powerful  

---

## **Step 1: Cloudinary Account তৈরি করুন**

1. যান: **https://cloudinary.com/users/register/free**
2. Email দিয়ে sign up করুন
3. Email verify করুন
4. Login করুন

---

## **Step 2: API Credentials পান**

1. Dashboard খুলুন: https://cloudinary.com/console/
2. এই details দেখবেন:
   ```
   Cloud Name: xxxxxxx
   API Key: 123456789
   API Secret: abcdefg123456
   ```
3. এগুলো save করুন (পরে লাগবে)

---

## **Step 3: .env ফাইল Update করুন**

আপনার **`.env`** ফাইল এ (project root এ):

```env
# Cloudinary Configuration
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

**Example:**
```env
CLOUDINARY_CLOUD_NAME=dxyz12345
CLOUDINARY_API_KEY=123456789
CLOUDINARY_API_SECRET=abcdefghijklmnop
```

---

## **Step 4: Django Setup (Already Done!)**

✅ **settings.py** - Already updated  
✅ **requirements.txt** - Already updated  
✅ **INSTALLED_APPS** - cloudinary added  
✅ **DEFAULT_FILE_STORAGE** - Cloudinary configured  

---

## **Step 5: Packages Install করুন**

```bash
pip install -r requirements.txt
```

---

## **Step 6: Test করুন**

```bash
python test_cloudinary.py
```

**Expected Output:**
```
✅ Cloudinary Connected!
✅ Upload Successful!
✅ Deletion Successful!
✅ All tests completed!
```

---

## **Usage Examples**

### **Example 1: Django Model এ ব্যবহার**

```python
# models.py
from django.db import models

class Product(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='products/')
    # Auto upload হবে Cloudinary এ
```

### **Example 2: View এ Cloudinary helper ব্যবহার**

```python
# views.py
from shop.cloudinary_helpers import upload_image, delete_image, get_thumbnail_url

def upload_product_image(request):
    if request.FILES['image']:
        result = upload_image(request.FILES['image'], 'products')
        
        if result:
            image_url = result['url']
            image_public_id = result['public_id']
            
            # Database এ save করুন
            product.image_url = image_url
            product.image_public_id = image_public_id
            product.save()
            
            return {'success': True, 'url': image_url}
    
    return {'success': False}
```

### **Example 3: Template এ Display**

```html
<!-- base.html -->
<img src="{{ product.image_url }}" alt="{{ product.title }}" 
     class="img-fluid" />

<!-- বা thumb generate করুন -->
{% load cloudinary %}
{% cloudinary product.image_public_id width=200 height=200 %}
```

### **Example 4: Different Image Sizes**

```python
from shop.cloudinary_helpers import get_optimized_url

# Small thumbnail
thumb = get_optimized_url(public_id, width=150, height=150)

# Medium image
medium = get_optimized_url(public_id, width=400, height=400)

# Large image
large = get_optimized_url(public_id, width=800)

# Using thumbnail helper
thumb = get_thumbnail_url(public_id, size=200)
```

### **Example 5: Video Upload**

```python
from shop.cloudinary_helpers import upload_video

def upload_product_video(request):
    if request.FILES.get('video'):
        result = upload_video(request.FILES['video'], 'product-videos')
        
        if result:
            video_url = result['url']
            video_duration = result['duration']  # Video duration in seconds
            
            return {'success': True, 'url': video_url}
```

---

## **Cloudinary Dashboard Features**

### **Media Library**
Dashboard এ যান: https://cloudinary.com/console/media_library

✅ Uploads history দেখুন  
✅ Manual upload করতে পারবেন  
✅ Transformations apply করতে পারবেন  
✅ Stats দেখতে পারবেন  

### **Storage Info**
```
Dashboard → Settings → Account
```

আপনার current usage দেখবেন:
- Used: X MB / 100 GB
- Transformations
- API calls

---

## **Django Admin এ Cloudinary Images**

Django admin এ image upload করতে এখনও local storage use হতে পারে। 

**Better approach:**
1. Admin এ "image URL" text field যোগ করুন
2. অথবা Cloudinary widget integrate করুন

```python
# models.py
class Product(models.Model):
    image_url = models.URLField(blank=True)
    # এর পরিবর্তে ImageField নয়, URLField ব্যবহার করুন
```

---

## **Production Setup (Render)**

Render এ environment variables set করুন:

```
CLOUDINARY_CLOUD_NAME = dxyz12345
CLOUDINARY_API_KEY = 123456789
CLOUDINARY_API_SECRET = abcdefghijk
```

**Render Dashboard:**
1. Project settings যান
2. "Environment" tab এ যান
3. এই 3টি variable add করুন

---

## **Troubleshooting**

### ❌ **"Cloudinary credentials not configured"**
**Solution:** 
- .env file চেক করুন
- Variable names correct আছে কি দেখুন
- Django restart করুন

### ❌ **"Unauthorized API Request"**
**Solution:**
- API Key সঠিক আছে কি চেক করুন
- API Secret copy paste করার সময় space নেই কি দেখুন

### ❌ **Image upload but URL broken**
**Solution:**
- Cloud Name সঠিক আছে কি দেখুন
- Cloudinary console এ public ID চেক করুন

---

## **Free Tier Limits**

```
Storage:          100 GB
Monthly uploads:  Unlimited
API calls:        500,000/month
Video duration:   25 hours/month
Transformations:  Unlimited
```

এই limits যথেষ্ট একটি ছোট-মাঝারি project এর জন্য!

---

## **Next Steps**

1. ✅ Cloudinary account create করুন
2. ✅ API credentials পান
3. ✅ .env file update করুন
4. ✅ Test script চালান
5. 🎉 আর Firebase billing নিয়ে চিন্তা নেই!

---

## **আরও তথ্য**

📚 **Official Docs**: https://cloudinary.com/documentation  
🎥 **Video Tutorials**: https://cloudinary.com/documentation/video_support  
🖼️ **Image Transformation**: https://cloudinary.com/documentation/image_transformation_reference  

Happy uploading! 🚀
