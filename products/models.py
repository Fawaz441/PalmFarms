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

    @property
    def farmer(self):
        return self.farm.farmer


class CartProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    delivered = models.BooleanField(default=False)

    def __str__(self):
        return self.product.name

    @property
    def total_cost(self):
        return self.product.selling_price * self.quantity


class Cart(models.Model):
    user = models.ForeignKey(
        User, related_name='basket', on_delete=models.SET_NULL, null=True, blank=True)
    items = models.ManyToManyField(CartProduct, blank=True)
    requires_dispatch = models.BooleanField(default=False)
    delivery_address = models.TextField()
    dispatch_rider = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="dispatch_orders")
    delivered = models.BooleanField(default=False)
    ordered = models.BooleanField(default=False)
    farmer = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True)
    ordered_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        if self.user:
            return self.user.full_name
        return self.id

    def total_cost(self):
        total = 0
        for item in self.items.all():
            total += item.total_cost
        return total


class DispatchApplication(models.Model):
    dispatch_rider = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Cart, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    accepted = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)


class Payment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    order = models.ForeignKey(
        Cart, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    reference = models.CharField(max_length=300)
    status = models.CharField(max_length=200)
    farmer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="farmer_payments")
    customer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="customer_payments")
