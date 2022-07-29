from django.utils import timezone


def get_midnight():
    now = timezone.now()
    midnight = timezone.datetime(
        now.year, now.month, now.day)
    return midnight


def date_hour(timestamp):
    return timestamp.strftime("%H:%M%p")


def date_month(timestamp):
    return timestamp.strftime("%b")
