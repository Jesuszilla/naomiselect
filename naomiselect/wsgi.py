"""
WSGI config for naomiselect project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "naomiselect.settings")

from django.core.wsgi import get_wsgi_application
#from whitenoise.django import DjangoWhiteNoise

from django.core.cache.backends.memcached import BaseMemcachedCache
BaseMemcachedCache.close = lambda self, **kwargs: None

application = get_wsgi_application()
#application = DjangoWhiteNoise(application)
