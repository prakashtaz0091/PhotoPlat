"""
ASGI config for project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from notifications import routing
from channels.auth import AuthMiddlewareStack

DJANGO_ENV = os.environ.get("DJANGO_ENV")

if DJANGO_ENV == "prod":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.prod")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.local")
   
 
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
        routing.websocket_urlpatterns
    )),
})