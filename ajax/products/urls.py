from django.urls import path
from ajax.products.views import adjust_product_quantity


urlpatterns = [
    path('adjust-product-quantity', adjust_product_quantity,
         name='adjust_product_quantity')
]
