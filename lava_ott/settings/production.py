from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*']

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

CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_HEADERS = [
    'access-control-allow-headers',
    'access-control-allow-methods',
    'access-control-allow-origin',
    'authorization',
    'content-type',
    'xauth',
]

OTP_SEND = True

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'nginx_error_log': {
#             'level': 'DEBUG',
#             'class': 'logging.handlers.WatchedFileHandler',
#             'filename': '/var/log/nginx/error.log',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['nginx_error_log'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#     },
# }
