from .base import *

DEBUG = True

ALLOWED_HOSTS = ['lavaott-979ac37aaaa6.herokuapp.com']


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

