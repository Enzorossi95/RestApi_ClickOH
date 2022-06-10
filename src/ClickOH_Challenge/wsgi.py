"""
WSGI settings for ClickOH_Challenge project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
if 'ENV' in os.environ and os.environ['ENV'] == 'development':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.docker")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.local")
#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.local')
print(get_wsgi_application())
application = get_wsgi_application()
