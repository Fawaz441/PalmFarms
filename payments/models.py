from django.db import models

WITHDRAWAL_REQUEST_STATES = (
    ("WITHDRAWN", "WITHDRAWN"),
    ("REJECTED", "REJECTED"),
    ("PENDING", "PENDING"),
)


class Wallet(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name if self.user else self.amount


class WithdrawalRequests(models.Model):
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(choices=WITHDRAWAL_REQUEST_STATES, max_length=20)
    sorted_time = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, blank=True, null=True)


class WalletTransaction(models.Model):
    description = models.TextField()
    created = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    wallet = models.ForeignKey(
        Wallet, on_delete=models.SET_NULL, null=True, blank=True)


class Bank(models.Model):
    bank_name = models.CharField(max_length=100)
    logo = models.FileField(null=True, blank=True)


class BankAccount(models.Model):
    account_number = models.CharField(max_length=10)
    bank = models.ForeignKey(
        Bank, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.bank_name
