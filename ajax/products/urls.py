from django.urls import path
from ajax.products.views import (
    adjust_product_quantity, get_payments, get_sales)


urlpatterns = [
    path('adjust-product-quantity', adjust_product_quantity,
         name='adjust_product_quantity'),
    path('get-payments', get_payments, name='get_payments'),
    path('get-sales', get_sales, name='get_sales')
]
