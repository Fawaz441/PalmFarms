"""
ASGI config for PalmFarms project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os
import dotenv
from django.core.asgi import get_asgi_application

SETTINGS = os.getenv("SETTINGS")

dotenv.read_dotenv(os.path.join(
    os.path.dirname(os.path.dirname(__file__)), '.env'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      SETTINGS)
application = get_asgi_application()
