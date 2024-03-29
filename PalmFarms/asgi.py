"""
ASGI config for PalmFarms project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os
import dotenv
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

dotenv.read_dotenv(os.path.join(
    os.path.dirname(os.path.dirname(__file__)), '.env'))

SETTINGS = os.getenv("SETTINGS")
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      SETTINGS)
django_asgi_app = get_asgi_application()
import chat.routing

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
    # Just HTTP for now. (We can add other protocols later.)
})
