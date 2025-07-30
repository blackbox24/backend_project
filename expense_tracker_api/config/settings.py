from pathlib import Path
from datetime import timedelta
from decouple import config, Csv

import logging

# Build paths inside the project like this: BASE_DIR / 'subdir'.
logging.basicConfig(level=logging.INFO)

BASE_DIR = Path(__file__).resolve().parent.parent
logger = logging.getLogger(__name__)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY",cast=str)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG",cast=bool,default=False)
logger.info(f"DEBUG: {DEBUG}")

ALLOWED_HOSTS = config("ALLOWED_HOSTS",cast=Csv())
logger.info(f"ALLOWED_HOSTS: {ALLOWED_HOSTS}")

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "drf_yasg",
    "guardian",
]

CUSTOM_APPS =  [
    "expense",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + CUSTOM_APPS

AUTHENTICATION_BACKENDS = [
    "guardian.backends.ObjectPermissionBackend",
    "django.contrib.auth.backends.ModelBackend",
]

SITE_ID = 1

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES":[
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    "DEFAULT_VERSIONING_CLASSES": [
        "rest_framework.versioning.URLPathVersioning",
    ]
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,

}

SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS":{
        "api_key":{
            "type": "apiKey",
            "name": "Authorization",
            "in": "header"
        }
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

USE_SQLITE = config("USE_SQLITE",cast=bool)
logger.info(f"USE_SQLITE: {USE_SQLITE}")

if USE_SQLITE:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    logger.error("No database select")


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = config("STATIC_ROOT",cast=str)

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    "version": 1,
    "disable_existing_logger": False,
    "formatters": {
        "verbose": {
            "style": "{",
            "format": "{levelname} {asctime} {message}",
        },
        "simple": {
            "style": "{",
            "format": "{levelname} {message}",
        }
    },
    "handlers":{
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "simple"
        },
        "file": {
            "class": "logging.FileHandler",
            "level": "WARNING",
            "formatter": "verbose",
            "filename": BASE_DIR / "warnings.log"
        }
    },
    "loggers":{
        "django": {
            "handlers": ["console","file"],
            "propagate": True
        },
        "expense.views": {
            "handlers": ["console","file"],
            "propagate": True
        }
    }
}
