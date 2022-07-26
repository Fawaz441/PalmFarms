from django.db import models
from products.models import Product
from accounts.models import User


class Goods(models.Model):
    products = models.ManyToManyField(Product)
    owner = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)


class DispatchBreakdown(models.Model):
    pass


class State(models.Model):
    name = models.CharField(max_length=100)
    capital = models.CharField(max_length=100)


class DispatchAddress(models.Model):
    state = models.ForeignKey(
        State, on_delete=models.SET_NULL, null=True, blank=True)
    street_address = models.TextField()


class Dispatch(models.Model):
    is_large_dispatch = models.BooleanField(default=False)
    goods = models.OneToOneField(
        Goods, on_delete=models.SET_NULL, null=True, blank=True, related_query_name="dispatch")
    dispatch_breakdown = models.ManyToManyField(DispatchBreakdown, blank=True)
    total_distance = models.FloatField(blank=True, null=True)
    total_dispatch_payment = models.DecimalField(
        max_digits=10, decimal_places=2)
    dispatch_tag = models.CharField(max_length=10, unique=True)
    dispatch_driver = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders")
    customer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="dispatches")
    current_dispatch_milestone = models.IntegerField(default=0)
    address = models.ForeignKey(
        DispatchAddress, on_delete=models.SET_NULL, null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    completed_date = models.DateTimeField(blank=True, null=True)

    @property
    def total_dispatch_milestones(self):
        return self.dispatch_breakdown.all().count() or 1
