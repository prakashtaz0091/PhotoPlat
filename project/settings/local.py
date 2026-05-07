from . base import *

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "main.middlewares.RequestMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]



JAZZMIN_SETTINGS = {
    "site_title": "PhotoPlat",
    "site_header": "PhotoPlat",
    "site_brand": "PhotoPlat",
    "show_ui_builder": True,    
}
JAZZMIN_UI_TWEAKS = {
    "theme": "minty",
    "dark_mode_theme": "darkly",
}

INTERNAL_IPS = [
    "127.0.0.1",
]