from django.contrib import admin
from .models import Product, ProductType, Cart, CartProduct
# Register your models here.

admin.site.register(Product)
admin.site.register(ProductType)
admin.site.register(Cart)
admin.site.register(CartProduct)
