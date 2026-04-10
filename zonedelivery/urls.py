from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

urlpatterns = i18n_patterns(
    path('', include('shop.urls')),   # shop অ্যাপের urls এখানে যোগ করা হলো
    prefix_default_language=True,
)

# Language change URL (i18n_patterns এর বাইরে)
urlpatterns += [
    path('i18n/', include('django.conf.urls.i18n')),
]

# Media files দেখানোর জন্য (localhost-এ ছবি দেখার জন্য)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)