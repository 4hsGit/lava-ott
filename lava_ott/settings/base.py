"""
Django settings for lava_ott project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-42zoh+(%^q^)$kypaa6ub83satxd_do!3x=it2kk4f#42m#hzl'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# import django_heroku
# import dj_database_url

# django_heroku.settings(locals())

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # new
    'rest_framework',
    'corsheaders',
    'storages',
    # local apps
    'users.apps.UsersConfig',
    'videos.apps.VideosConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # local
    'users.middleware.CustomMiddleWare',
]

ROOT_URLCONF = 'lava_ott.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'lava_ott.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# STATIC_FILES_DIRS = [os.path.join(BASE_DIR, 'static')]
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# MEDIA_ROOT = os.path.join(BASE_DIR, 'lavaott_media')
MEDIA_URL = 'lavaott_media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.User'

AUTHENTICATION_BACKENDS = [
    'users.custom_authentication.AdminAuthenticationBackend',
    'users.custom_authentication.AppAuthenticationBackend'
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ]
}

CSRF_FAILURE_VIEW = 'users.error_handler_views.error_403_view'

# SESSION_COOKIE_AGE = 10
# SESSION_SAVE_EVERY_REQUEST = True
# SESSION_ENGINE = 'django.contrib.sessions.backends.db'

ADMIN_SESSION_AGE = 300  # In seconds
USER_KEEP_SESSION_AGE = 300  # In seconds
USER_SESSION_AGE = 300  # In seconds

# CORS_ALLOWED_ORIGINS = ['https://lavaott-979ac37aaaa6.herokuapp.com']

# AWS S3 Bucket Conf

AWS_ACCESS_KEY_ID = 'AKIAQ3EGQOD37YLYDA5E' # Local Code
# AWS_ACCESS_KEY_ID = 'AKIAQ3EGQOD3UM3TO7EH' # Third Party
# AWS_ACCESS_KEY_ID = 'AKIAQ3EGQOD3ZSU7I4FG' # Other
AWS_SECRET_ACCESS_KEY = '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' # Local Code
# AWS_SECRET_ACCESS_KEY = 'l6IyrAC99Wzo+enOYSHRbzwU1DYRnwKDjPv1B5Ck' # Third Party
# AWS_SECRET_ACCESS_KEY = '0GO1NfukevXvVbXT79YAqxZcC0myVfA+4/3H4Qr/' # Other
AWS_STORAGE_BUCKET_NAME = 'lavao-bucket'
AWS_S3_REGION_NAME = 'ap-south-1'

AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

# For serving static files directly from S3
AWS_S3_URL_PROTOCOL = 'https:'
# AWS_S3_USE_SSL = True
AWS_S3_VERIFY = True

AWS_DEFAULT_ACL = None

# Static and media file configuration
# STATIC_URL = f'{AWS_S3_URL_PROTOCOL}//{AWS_S3_CUSTOM_DOMAIN}/static/'
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# MEDIA_URL = f'{AWS_S3_URL_PROTOCOL}//{AWS_S3_CUSTOM_DOMAIN}/media/'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
