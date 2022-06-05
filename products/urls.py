from django.urls import path
from .views import (AddProductView, ProductListView,
                    PaymentListView, CheckoutView, AddToCart, ConfirmBankPayment,
                    AttachDispatchRider, ConfirmPayment)

urlpatterns = [
    path('add-product', AddProductView.as_view(), name='add-product'),
    path('farms', ProductListView.as_view(), name='farms'),
    path('payments', PaymentListView.as_view(), name='payments'),
    path('checkout', CheckoutView.as_view(), name='checkout'),
    path('add-to-cart/<int:product_id>',
         AddToCart.as_view(), name='add-to-cart'),
    path('confirm-bank-payment', ConfirmBankPayment.as_view(),
         name="confirm-bank-payment"),
    path('attach-dispatch-rider', AttachDispatchRider.as_view(),
         name='attach_dispatch_rider'),
    path('confirm-payment', ConfirmPayment.as_view(), name='confirm_payment')
]
