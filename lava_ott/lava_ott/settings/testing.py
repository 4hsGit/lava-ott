from .base import *

ALLOWED_HOSTS = ['*']

import django_heroku
import dj_database_url

django_heroku.settings(locals())