from random import randint
from urllib.parse import urlparse

import requests
from accounts.models import Farm
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from products.models import Product, ProductType

types = ["Vegetables", "Fruits", "Cash Crop", "Grains", "Tubers", "Spices"]

url = "https://www.ec.europa.eu/agrifood/api/fruitAndVegetable/prices?memberStateCodes=PT,SI&products=oranges&months=1,2,3&beginDate=12/02/2018&endDate=23/03/2020"
image_url = "https://cdn.pixabay.com/photo/2018/02/19/18/15/potatoes-3165753__340.jpg"


class Command(BaseCommand):
    def handle(self, *args, **options):
        req = requests.get(url)
        if req.ok:
            data = req.json()
            for item in data:
                product_type, _ = ProductType.objects.get_or_create(
                    name=item['variety'])
                product = Product(
                    name=item["product"],
                    cost_price=randint(100, 1000),
                    selling_price=randint(100, 1000),
                    type=product_type,
                    farm=Farm.objects.first()
                )
                product_name = urlparse(image_url).path.split('/')[-1]
                response = requests.get(image_url)
                if response.status_code == 200:
                    product.image.save(product_name, ContentFile(
                        response.content), save=True)
                product.save()
        else:
            print("Failed")
