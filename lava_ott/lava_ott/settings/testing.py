from .base import *

ALLOWED_HOSTS = ['lavaott-test-f146afb30529.herokuapp.com']

import django_heroku
import dj_database_url

django_heroku.settings(locals())
