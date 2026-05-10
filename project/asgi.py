import os
from dotenv import load_dotenv
from channels.auth import AuthMiddlewareStack


DJANGO_ENV = os.environ.get("DJANGO_ENV")

if DJANGO_ENV == "prod":
    load_dotenv(".env.production")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.prod")
else:
    load_dotenv(".env.local")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.local")

# All imports that touch Django MUST come after env setup
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from notifications import routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
        routing.websocket_urlpatterns
    )),
})