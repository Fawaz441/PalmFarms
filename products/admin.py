from django.contrib import admin
from .models import Product, ProductType, Cart, CartProduct, DispatchApplication, Payment, Coupon
# Register your models here.

admin.site.register(Product)
admin.site.register(ProductType)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(DispatchApplication)
admin.site.register(Payment)
admin.site.register(Coupon)
