from django.urls import path
from .views import AddProductView, ProductListView, PaymentListView

urlpatterns = [
    path('add-product', AddProductView.as_view(), name='add-product'),
    path('farms', ProductListView.as_view(), name='farms'),
    path('payments', PaymentListView.as_view(), name='payments')
]
