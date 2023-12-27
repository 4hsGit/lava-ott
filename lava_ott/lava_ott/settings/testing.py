from .base import *

ALLOWED_HOSTS = ['bibinab.pythonanywhere.com']

import django_heroku
import dj_database_url

django_heroku.settings(locals())