from .base import *

DEBUG = False

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
