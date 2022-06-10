from .base import *
from decouple import config

DATABASES = {
    'default': {
        "ENGINE": 'django.db.backends.postgresql',
        "NAME": config("POSTGRES_DB_DOCKER", default="postgres"),
        "HOST": config("POSTGRES_HOST_DOCKER", default="db"),
        "PORT": config("POSTGRES_PORT", default=5432),
        "USER": config("POSTGRES_USER"),
        "PASSWORD": config("POSTGRES_PASS_DOCKER"),
    }
}

STATIC_ROOT = '/static/'