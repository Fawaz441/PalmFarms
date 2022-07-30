from django.core.management.base import BaseCommand
from django.utils import timezone
from accounts.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        users = User.objects.filter(date_joined__isnull=True)
        date = timezone.datetime(2022, 5, 19)
        users.update(date_joined=date)
