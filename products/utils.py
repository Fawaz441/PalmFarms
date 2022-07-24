from random import choice
import string
from django.utils.dates import MONTHS
from django.utils import timezone
from products.models import Payment


def get_months_options():
    months = []
    month_keys = list(MONTHS.keys())
    for key in month_keys:
        months.append({'value': key, 'label': MONTHS[key]})
    return months


def generate_reference():
    ref = ""
    for i in range(20):
        ref += choice(string.ascii_letters)
    return ref


def confirm_bank_payment(order, amount, reference=None):
    order.delivery_address = "Just a random address"
    order.ordered = True
    new_ref = f"ORDER--{order.id}--{order.user.id}"
    order.reference = new_ref
    order.ordered_date = timezone.now()
    order.save()
    order.refresh_from_db()
    Payment.objects.create(
        amount=amount,
        reference=new_ref or reference,
        status="Pending Confirmation",
        farmer=order.items.first().product.farmer,
        customer=order.user
    )


def generate_tag(length):
    return ''.join(choice(string.ascii_uppercase + string.digits)
                   for _ in range(length))
