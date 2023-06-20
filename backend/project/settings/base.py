from datetime import timedelta
from os import path, mkdir
from os.path import join, exists
from pathlib import Path

from psycopg2 import OperationalError

from .config_data import (
    KEY, EMAIL_SERVER, EMAIL_PASSWORD,
    SQL_PASSWORD, SQL_USER,
    SQL_DB, SQL_PORT, SQL_HOST,
    SQL_ENGINE
)

BASE_DIR = Path(__file__).resolve().parent.parent
GENERAL_DIR = BASE_DIR.parent
DB_DIR = GENERAL_DIR / 'db'

SECRET_KEY = KEY

DEBUG = True

ALLOWED_HOSTS = ['*']

NEW_ADMIN = [
    'material',
    'material.admin',
]

DJANGO_DEFAULT_APPS = [
    # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

DOWNLOADED_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_resized',
    'django_cleanup.apps.CleanupConfig'
]

PROJECT_APPS = [
    'project.apps.authorization',
    'project.apps.crm'
]

INSTALLED_APPS = NEW_ADMIN + DJANGO_DEFAULT_APPS + DOWNLOADED_APPS + PROJECT_APPS
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8080',
    'http://localhost',
    'http://185.233.119.142:8080',
    'http://185.233.119.142:8000',
    'http://185.233.119.142:80',
]

CORS_ALLOW_ALL_ORIGINS = True
# CORS_ALLOWED_ORIGINS = [
#     'http://localhost:8080',
#     'http://localhost',
#     'http://185.233.119.142:8080',
#     'http://185.233.119.142:8000',
#     'http://185.233.119.142:80',
# ]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

AUTH_USER_MODEL = 'authorization.User'
AUTH_PROFILE_MODULE = 'authorization.Profile'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [GENERAL_DIR / 'templates'],
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

WSGI_APPLICATION = 'project.network.wsgi.application'

# DATABASES = {
#     'default': {
#         "ENGINE": SQL_ENGINE or "django.db.backends.sqlite3",
#         "NAME": SQL_DB or DB_DIR / 'db.sqlite3',
#         "USER": SQL_USER or "user",
#         "PASSWORD": SQL_PASSWORD or "password",
#         "HOST": SQL_HOST or "localhost",
#         "PORT": SQL_PORT or "5432",
#     }}

DATABASES = {
    'default': {
        "ENGINE": SQL_ENGINE,
        "NAME": SQL_DB,
        "USER": SQL_USER,
        "PASSWORD": SQL_PASSWORD,
        "HOST": SQL_HOST,
        "PORT": SQL_PORT,
    },
    'sqlite': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DB_DIR / 'db.sqlite3',
    }}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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

STATIC_URL = '/static/'
STATIC_ROOT = join(GENERAL_DIR, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = join(GENERAL_DIR, 'media')

NAME_BASE_STATIC_DIRS = '/developer_static/'

FOLDERS_FOR_CREATE = ['db', "developer_static"]

STATICFILES_DIRS = (
    join(GENERAL_DIR, f"{GENERAL_DIR}{NAME_BASE_STATIC_DIRS}"),
)

for folder in FOLDERS_FOR_CREATE:
    if not exists(f'{GENERAL_DIR}/{folder}'):
        mkdir(f'{GENERAL_DIR}/{folder}')

LANGUAGE_CODE = 'RU'

TIME_ZONE = 'Europe/Kiev'

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = EMAIL_SERVER
EMAIL_HOST_PASSWORD = EMAIL_PASSWORD

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,

    "ALGORITHM": "HS256",
    "SIGNING_KEY": KEY,
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,

    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}
