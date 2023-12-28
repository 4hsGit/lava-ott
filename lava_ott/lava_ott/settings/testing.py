from .base import *

DEBUG = False

ALLOWED_HOSTS = ['lavaott-1-be4120441dfc.herokuapp.com']

import django_heroku
import dj_database_url

django_heroku.settings(locals())
