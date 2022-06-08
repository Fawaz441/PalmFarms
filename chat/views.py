from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from accounts.models import User, FARMER
from .models import Channel


@login_required
def index(request):
    if not request.user.is_farmer:
        print('not a farmer')
        farmers = User.objects.filter(
            user_type=FARMER)
        for farmer in farmers:
            channel, _ = Channel.objects.get_or_create(
                seller=farmer, purchaser=request.user)
    channels = Channel.objects.filter(
        Q(seller=request.user) |
        Q(purchaser=request.user)
    )
    return render(request, 'chat/index.html', {'channels': channels})


def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })
