from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
]

# Media files দেখানোর জন্য (localhost-এ ছবি দেখার জন্য)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)