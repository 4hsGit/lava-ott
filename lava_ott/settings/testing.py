from .base import *

DEBUG = True

ALLOWED_HOSTS = ['lavaott-979ac37aaaa6.herokuapp.com']

import django_heroku

django_heroku.settings(locals())
