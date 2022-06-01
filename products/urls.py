from django.urls import path
from .views import AddProductView, ProductListView

urlpatterns = [
    path('add-product', AddProductView.as_view(), name='add-product'),
    path('farms', ProductListView.as_view(), name='farms')
]
