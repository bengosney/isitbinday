# Standard Library
import logging
import os

# Third Party
import dj_database_url

# Locals
from .base import *  # noqa
from .base import DATABASES, MIDDLEWARE

logger = logging.getLogger(__name__)

DEBUG = False

env = os.environ.copy()

ALLOWED_HOSTS = ["localhost:8000", "localhost"] + env["ALLOWED_HOSTS"].split(",")

BASE_URL = env["BASE_URL"]

CSRF_TRUSTED_ORIGINS = [
    BASE_URL,
]

DATABASES["default"] = dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SECRET_KEY = env["SECRET_KEY"]

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

MIDDLEWARE += [
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

# STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
THUMBNAIL_DEFAULT_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = "isitbinday"
AWS_S3_REGION_NAME = "eu-west-2"
AWS_QUERYSTRING_AUTH = False

AWS_S3_OBJECT_PARAMETERS = {
    "Expires": "Thu, 31 Dec 2099 20:00:00 GMT",
    "CacheControl": "max-age=94608000",
}

# AWS_S3_CUSTOM_DOMAIN = "cdn.isitbinday.com"

# DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

try:
    EMAIL_HOST = env["SMTP_HOST"]
    EMAIL_HOST_USER = env["SMTP_USER"]
    EMAIL_HOST_PASSWORD = env["SMTP_PASS"]
    EMAIL_PORT = env["SMTP_PORT"]
    EMAIL_USE_TLS = (env.get("SMTP_TLS", "True") or "True") != "False"
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
except KeyError as e:
    logger.warning(f"Missing SMTP environment variable: {e}")

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "default",
    },
    "renditions": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "renditions",
    },
}
