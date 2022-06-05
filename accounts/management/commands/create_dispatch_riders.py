from django.core.management.base import BaseCommand
from accounts.models import User

password = 'password'
users = [
    {'f_name': 'Dispatch Rider 1', 'surname': 'dispatch', 'phone': '+2348123456790', },
    {'f_name': 'Dispatch Rider 2', 'surname': 'dispatch', 'phone': '+2348123456791', },
    {'f_name': 'Dispatch Rider 3', 'surname': 'dispatch', 'phone': '+2348123456792', },
]


class Command(BaseCommand):
    def handle(self, *args, **options):
        for user in users:
            User.objects.create(
                full_name=user.get('f_name'),
                surname=user.get('surname'),
                phone_number=user.get('phone'),
                user_type='DISPATCH RIDER'
            )
