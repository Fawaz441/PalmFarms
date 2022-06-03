from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from PalmFarms.views import LandingPage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPage.as_view(), name='landing-page'),
    path('', include(('products.urls', 'products'))),
    path('accounts/', include(('accounts.urls', 'accounts'))),
    path('ajax/', include(('ajax.urls', 'ajax')))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
