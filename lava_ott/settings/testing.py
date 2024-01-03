from .base import *

DEBUG = True

ALLOWED_HOSTS = []

import django_heroku

django_heroku.settings(locals())
