# Locals
from .base import *  # noqa
from .base import INSTALLED_APPS, MIDDLEWARE

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-fn8#(5r4vbabxql*u_*e+-%j#4^7g__nh@o05$$%m^6=asx+s@"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


INSTALLED_APPS += [
    "debug_toolbar",
    "django_browser_reload",
]

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django_browser_reload.middleware.BrowserReloadMiddleware",
    "kolo.middleware.KoloMiddleware",
]

INTERNAL_IPS = [
    "127.0.0.1",
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "incremental": True,
    "root": {
        "level": "DEBUG",
    },
}

CSP_DEFAULT_SRC = None
CSP_STYLE_SRC = None
CSP_FONT_SRC = None
CSP_IMG_SRC = None

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
