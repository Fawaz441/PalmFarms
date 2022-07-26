from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.api.views import CustomRegisterView, CustomLoginView, CustomLogoutView

from PalmFarms.views import LandingPage, AboutPage, FAQPage, ContactUsPage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPage.as_view(), name='landing-page'),
    path('about', AboutPage.as_view(), name='about'),
    path('faq', FAQPage.as_view(), name='faq'),
    path('contact-us', ContactUsPage.as_view(), name='contact-us'),
    path('', include(('products.urls', 'products'))),
    path('accounts/', include(('accounts.urls', 'accounts'))),
    path('chat/', include(('chat.urls', 'chat'))),
    path('ajax/', include(('ajax.urls', 'ajax'))),

    path('api/v1/signup/', CustomRegisterView.as_view(), name='register'),
    path('api/v1/login', CustomLoginView.as_view(), name='login'),
    path('api/v1/logout/', CustomLogoutView.as_view(), name='logout'),
    path("api/v1/consulting/", include(("consulting.api.urls", "consulting"))),
    path("api/v1/products/", include(("products.api.urls", "products-api"))),
    path("api/v1/dispatching/", include(("dispatching.api.urls", "dispatching"))),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
