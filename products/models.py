from django.db import models
from django.conf import settings
from accounts.models import User, Farm


class ProductType(models.Model):
    name = models.CharField(max_length=1000, unique=True)

    def __str__(self):
        return self.name


class ProductVariation(models.Model):
    name = models.CharField(max_length=200)


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
    discount = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    variations = models.ManyToManyField(ProductVariation, blank=True)
    tag = models.CharField(max_length=100, unique=True)
    start_date = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name

    @property
    def farmer(self):
        return self.farm.farmer

    @property
    def product_image(self):
        if self.image:
            if settings.IS_DEV:
                return f"{settings.BASE_URL}{self.image.url}"
            return self.image.url
        return None


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


class Coupon(models.Model):
    is_amount = models.BooleanField(default=False)
    max_use = models.IntegerField(default=1)
    code = models.CharField(max_length=10)
    expired = models.BooleanField(default=False)
    value = models.IntegerField()
    expiry_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.code


class Cart(models.Model):
    user = models.ForeignKey(
        User, related_name='basket', on_delete=models.SET_NULL, null=True, blank=True)
    items = models.ManyToManyField(CartProduct, blank=True)
    requires_dispatch = models.BooleanField(default=False)
    delivery_address = models.ForeignKey(
        "dispatching.DispatchAddress", on_delete=models.SET_NULL, null=True, blank=True)
    dispatch_rider = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="dispatch_orders")
    delivered = models.BooleanField(default=False)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(blank=True, null=True)
    reference = models.CharField(max_length=100)
    coupon = models.ForeignKey(
        Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    delivery_fee = models.DecimalField(
        max_digits=10, decimal_places=2, default=1000)

    def __str__(self):
        if self.user:
            return self.user.full_name
        return self.id

    def subtotal(self):
        total = 0
        for item in self.items.all():
            total += item.total_cost
        return total

    def total_cost(self):
        total = self.delivery_fee
        for item in self.items.all():
            total += item.total_cost
        coupon = self.coupon
        if coupon:
            if coupon.is_amount:
                total = total - coupon.value
            else:
                total = (coupon.value/100) * total
            if total < 0:
                return 0
        return total

    def discount(self):
        coupon = self.coupon
        if coupon:
            if coupon.is_amount:
                return coupon.value
            return self.subtotal() * (coupon.value/100)


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
    customer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="customer_payments")

    def __str__(self):
        return self.reference


class Purchase(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    customer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    time = models.DateTimeField(auto_now=True)
    farmer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="sales")
