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
print('base dir -> ', BASE_DIR)
# BASE_DIR = Path(__file__).resolve().parent.parent

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

    # 'whitenoise.middleware.WhiteNoiseMiddleware',

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
        'DIRS': ["C:/Users/sanja/Bibin/"],
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

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# STATIC_URL = 'static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# STATIC_FILES_DIRS = [os.path.join(BASE_DIR, 'static')]
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# MEDIA_ROOT = os.path.join(BASE_DIR, 'static', 'lavaott_media')
# MEDIA_URL = 'lavaott-media/'

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

ADMIN_SESSION_AGE = 3000  # In seconds
USER_KEEP_SESSION_AGE = 300 * 86400  # In seconds
USER_SESSION_AGE = 30 * 86400  # In seconds

# CORS_ALLOWED_ORIGINS = ['https://lavaott-979ac37aaaa6.herokuapp.com']

# AWS S3 Bucket Conf
#
AWS_ACCESS_KEY_ID = 'AKIAQ3EGQOD37LQE7U4C' # Local Code
# AWS_ACCESS_KEY_ID = 'AKIAQ3EGQOD3UM3TO7EH' # Third Party
# AWS_ACCESS_KEY_ID = 'AKIAQ3EGQOD3XT7WVM5L' # Other
# AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = '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' # Local Code
# AWS_SECRET_ACCESS_KEY = 'l6IyrAC99Wzo+enOYSHRbzwU1DYRnwKDjPv1B5Ck' # Third Party
# AWS_SECRET_ACCESS_KEY = 'XsgDZ6RY0YOCc+eqwJ9RPDQW4Tqo5E//9uBvHYgG' # Other
# AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'lavao-bucket'
AWS_S3_REGION_NAME = 'ap-south-1'

AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

# For serving static files directly from S3
AWS_S3_URL_PROTOCOL = 'https:'
# AWS_S3_USE_SSL = True
# AWS_S3_VERIFY = True

# AWS_DEFAULT_ACL = None

# Static and media file configuration
STATIC_URL = f'{AWS_S3_URL_PROTOCOL}//{AWS_S3_CUSTOM_DOMAIN}/static/'
# STATIC_ROOT = f'{AWS_S3_URL_PROTOCOL}//{AWS_S3_CUSTOM_DOMAIN}'
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

MEDIA_URL = f'{AWS_S3_URL_PROTOCOL}//{AWS_S3_CUSTOM_DOMAIN}/'
# MEDIA_ROOT = f'{AWS_S3_URL_PROTOCOL}//{AWS_S3_CUSTOM_DOMAIN}'
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


# ----- OTP ----- #
OTP_SEND = True

OTP_API_KEY = 'c744a792-cf26-11ee-8cbb-0200cd936042'

OTP_SEND_URL = 'https://2factor.in/API/V1/{}/SMS/{}/AUTOGEN/OTP_2'  # Main
# OTP_SEND_URL = 'https://2factor.in/API/V1/{}/SMS/{}/AUTOGEN2/OTP_2'
# OTP_SEND_URL = 'https://2factor.in/API/V1/{}/SMS/{}/AUTOGEN3/OTP_2'
# OTP_SEND_URL = 'https://2factor.in/API/V1/{}/SMS/{}/1111/OTP_2'

OTP_VERIFY_URL = 'https://2factor.in/API/V1/{}/SMS/VERIFY3/{}/{}'

VERIFIED_NUMBERS = ['8075554765']
VERIFIED_OTPS = ['123456']
BY_PASS_VERIFY = True
