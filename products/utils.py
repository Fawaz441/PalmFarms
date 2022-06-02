from random import choice
import string
from products.models import Payment


def generate_reference():
    ref = ""
    for i in range(20):
        ref += choice(string.ascii_letters)
    return ref


def confirm_bank_payment(order, amount, reference=None):
    order.delivery_address = "Just a random address"
    order.ordered = True
    order.save()
    order.refresh_from_db()
    Payment.objects.create(
        amount=amount,
        reference=reference or generate_reference(),
        status="Pending Confirmation",
        farmer=order.items.first().product.farmer,
        customer=order.user
    )
