"""
WSGI config for sparks project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sparks.settings")

from django.core.handlers.wsgi import WSGIHandler
from whitenoise.django import DjangoWhiteNoise


class StaffDebugWSGIHandler(WSGIHandler):
    "WSGI Handler that shows the debug error page if the logged in user is staff"

    def handle_uncaught_exception(self, request, resolver, exc_info):
        "Return a debug page response if the logged in user is staff"
        import logging
        logger = logging.getLogger('etch.wsgi')

        from django.conf import settings

        if not settings.DEBUG and hasattr(request, 'user') and request.user.is_staff:
            from django.views import debug
            return debug.technical_500_response(request, *exc_info)

        logger.exception('There was an uncaught exception')

        # not logged in or not a staff user, display normal public 500
        return super(StaffDebugWSGIHandler, self).handle_uncaught_exception(request, resolver, exc_info)


application = DjangoWhiteNoise(StaffDebugWSGIHandler())
