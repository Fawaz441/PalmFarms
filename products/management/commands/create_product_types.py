from django.core.management.base import BaseCommand
from products.models import ProductType

types = ["Vegetables", "Fruits", "Cash Crop", "Grains", "Tubers", "Spices"]


class Command(BaseCommand):
    def handle(self, *args, **options):
        for type in types:
            ProductType.objects.create(name=type)
        print("**product types creaated**")
