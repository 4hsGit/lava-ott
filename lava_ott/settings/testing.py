from .base import *

DEBUG = True

ALLOWED_HOSTS = ['164.52.218.69']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'lavapdn',
        'USER': 'lava',
        'PASSWORD': 'ayMocMo9ZBxS8n3',
        'HOST': 'localhost',
        'PORT': '',
    }
}

CORS_ALLOW_ALL_ORIGINS = True
# CORS_ALLOWED_ORIGINS = [
#     r'^http://*$',
#     r'^https://*$',
    # 'http://localhost:3000'
# ]
CORS_ALLOW_HEADERS = [
    'access-control-allow-headers',
    'access-control-allow-methods',
    'access-control-allow-origin',
    'authorization',
    'content-type',
    'xauth',
]
