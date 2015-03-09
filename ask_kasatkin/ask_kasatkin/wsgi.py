"""
WSGI config for ask_kasatkin project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ask_kasatkin.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# -- run it with current configs --
# gunicorn ask_kasatkin.wsgi:application --bind localhost:7000 --daemon