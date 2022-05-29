from django.contrib import admin
from django.urls import path, include

from PalmFarms.views import LandingPage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPage.as_view(), name='landing-page'),
    path('accounts/', include(('accounts.urls', 'accounts')))
]
