from .settings import *

INSTALLED_APPS = INSTALLED_APPS + (
    'raven.contrib.django.raven_compat',
)

ENVIRONMENT = 'prod'

RAVEN_CONFIG = {
    'dsn': 'https://599822454b0e476aacf62458f65982d9:bc58c995ca6d4286904b0ba2de21c422@app.getsentry.com/34410',
}
