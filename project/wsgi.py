import os
from dotenv import load_dotenv
from django.core.wsgi import get_wsgi_application

DJANGO_ENV = os.getenv("DJANGO_ENV", "local")


if DJANGO_ENV == "prod":
    load_dotenv(".env.production")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.prod")
else:
    load_dotenv(".env.local")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.local")
    

application = get_wsgi_application()
