from django.urls import path, include

urlpatterns = [
    path('products/', include(('ajax.products.urls', 'products')))
]