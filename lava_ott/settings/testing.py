from .base import *

DEBUG = True

ALLOWED_HOSTS = ['lavaott-979ac37aaaa6.herokuapp.com']


CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = ['*']
CORS_ALLOW_CREDENTIALS = True

import django_heroku

django_heroku.settings(locals())

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
