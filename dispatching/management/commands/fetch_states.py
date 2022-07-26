import requests
from django.core.management.base import BaseCommand
from dispatching.models import State


class Command(BaseCommand):
    def handle(self, *args, **options):
        url = "https://nigerian-states-info.herokuapp.com/api/v1/states"
        response = requests.get(url)
        data = response.json().get("data")
        for item in data:
            item = item.get("info")
            state = item.get("officialName")
            capital = item.get("Capital")
            State.objects.create(name=state, capital=capital)
            print(f"created state {state}")
        State.objects.create(name="FCT", capital="Abuja")
        print(f"created FCT too....")
