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
SECRET_KEY = 'f)-7*k0b@(49ek*yx*!-_1+a+ss%4yubw7^z2%6a_wxd%#ab)y'

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
    'raven.contrib.django.raven_compat',
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
}

CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

RAVEN_CONFIG = {
    'dsn': 'https://599822454b0e476aacf62458f65982d9:bc58c995ca6d4286904b0ba2de21c422@app.getsentry.com/34410',
}
