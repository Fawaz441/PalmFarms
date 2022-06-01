from operator import mod
from django.db import models
from accounts.models import User, Farm


class ProductType(models.Model):
    name = models.CharField(max_length=1000, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=500)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products')
    is_active = models.BooleanField(default=True)
    available_stock = models.IntegerField(default=1)
    type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    rating = models.IntegerField(null=True, blank=True)
    farm = models.ForeignKey(Farm, related_name='farm_products',
                             on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class CartProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    delivered = models.BooleanField(default=False)


class Cart(models.Model):
    user = models.OneToOneField(
        User, related_name='basket', on_delete=models.CASCADE)
    items = models.ManyToManyField(CartProduct, blank=True)
