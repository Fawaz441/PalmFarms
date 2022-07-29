from django.utils import timezone


def get_midnight():
    now = timezone.now()
    midnight = timezone.datetime(
        now.year, now.month, now.day)
    return midnight
