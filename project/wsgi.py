import os
from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv

DJANGO_ENV = os.environ.get("DJANGO_ENV")

if DJANGO_ENV == "prod":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.prod")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.local")
    


application = get_wsgi_application()
