"""
Django settings for sparks project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
from datetime import timedelta
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', '123')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 1) == 1

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']
ENVIRONMENT = 'dev'

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social.apps.django_app.default',
    "djcelery",
    'kombu.transport.django',
    "sparksasync",
    "sparksbase",
    "paper",
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'sparks.urls'

WSGI_APPLICATION = 'sparks.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Parse database configuration from $DATABASE_URL
import dj_database_url
defaulted = os.environ.get('WERCKER_POSTGRESQL_URL', 'sqlite://./data.sql')
DATABASES['default'] = dj_database_url.config(default=defaulted)

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static asset configuration
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Celery
import djcelery
djcelery.setup_loader()
redis_location = os.environ.get('REDISCLOUD_URL', 'redis://127.0.0.1:6379')

BROKER_URL = os.environ.get('RABBITMQ_BIGWIG_URL', 'redis://127.0.0.1:6379/0')
CELERY_RESULT_BACKEND = os.environ.get('RABBITMQ_BIGWIG_URL', 'redis://127.0.0.1:6379/1')
CELERY_CREATE_MISSING_QUEUES = True

CELERY_ROUTES = {'sparksasync.tasks.urlopen': {'queue': 'http'}}

UNIT_TESTING = False

CELERYBEAT_SCHEDULE = {
    'update_rss': {
        'task': 'paper.tasks.update_rss',
        'schedule': timedelta(minutes=5),
    },
    'process_rss': {
        'task': 'paper.tasks.process_rss',
        'schedule': timedelta(minutes=5),
    },
    'process_articles': {
        'task': 'paper.tasks.process_articles',
        'schedule': timedelta(minutes=5),
    },
    'update_facebook': {
        'task': 'paper.tasks.update_facebook',
        'schedule': timedelta(minutes=5),
    },
}

CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry', 'console'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}

SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['username', 'first_name', 'email']
SOCIAL_AUTH_POCKET_CONSUMER_KEY = os.environ.get('SOCIAL_AUTH_POCKET_CONSUMER_KEY', '123')

AUTHENTICATION_BACKENDS = (
    'social.backends.pocket.PocketAuth',
    'django.contrib.auth.backends.ModelBackend',
)
