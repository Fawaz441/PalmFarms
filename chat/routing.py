from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<farmer_id>\w+)/(?P<customer_id>\w+)/$',
            consumers.ChatConsumer.as_asgi()),
]
