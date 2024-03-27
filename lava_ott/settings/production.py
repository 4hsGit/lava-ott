from .base import *

DEBUG = False

ALLOWED_HOSTS = ['65.0.75.137']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mylava',
        'USER': 'mylavauser',
        'PASSWORD': 'mylava@2024',
        'HOST': 'localhost',
        'PORT': '',
    }
}

CORS_ALLOW_HEADERS = [
    'access-control-allow-headers',
    'access-control-allow-methods',
    'access-control-allow-origin',
    'authorization',
    'content-type',
    'xauth',
]

OTP_SEND = True