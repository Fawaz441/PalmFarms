from django.db import models
from accounts.models import User


class Wallet(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(
        User, on_delete=models.SET_NULL, related_name="wallet", null=True, blank=True)

    def __str__(self):
        return self.user.first_name if self.user else self.amount
