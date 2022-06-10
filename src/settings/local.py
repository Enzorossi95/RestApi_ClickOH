from .base import *
from decouple import config

DATABASES = {
    'default': {
        "ENGINE": 'django.db.backends.postgresql',
        "NAME": config("POSTGRES_DB", default="app"),
        "HOST": config("POSTGRES_HOST", default="127.0.0.1"),
        "PORT": config("POSTGRES_PORT", default=5432),
        "USER": config("POSTGRES_USER"),
        "PASSWORD": config("POSTGRES_PASS"),
    }
}