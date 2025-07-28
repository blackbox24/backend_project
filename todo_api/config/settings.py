from pathlib import Path
from decouple import config
import os
import logging

# Build paths inside the project like this: BASE_DIR / 'subdir'.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY",cast=str,default="secret")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG",cast=bool,default=False)
logger.info(f"DEBUG: {DEBUG}")

ALLOWED_HOSTS = config("ALLOWED_HOSTS").split(",")
logger.info(f"ALLOWED_HOSTS: {ALLOWED_HOSTS}")


# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django.contrib.sites",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework.authtoken",

    "corsheaders",

    "drf_yasg",

    "guardian",
    "dj_rest_auth",
    'dj_rest_auth.registration',

    "allauth",
    "allauth.account",
    'allauth.socialaccount',
]

CUSTOM_APPS = [
    "todo",
]

SITE_ID = 1

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + CUSTOM_APPS

CORS_ALLOWED_ORIGINS = config("CSRF_TRUSTED_ORIGINS").split(",")
logger.info(f"CORS_ALLOWED_ORIGINS: {CORS_ALLOWED_ORIGINS}")

CSRF_TRUSTED_ORIGINS = config("CSRF_TRUSTED_ORIGINS").split(",")
logger.info(f"CSRF_TRUSTED_ORIGINS: {CSRF_TRUSTED_ORIGINS}")

AUTHENTICATION_BACKENDS = [
    "guardian.backends.ObjectPermissionBackend",
    "django.contrib.auth.backends.ModelBackend"
]

try:
    import redis
    r = redis.Redis(
        host=config("REDIS_HOST",cast=str),
        port=config("REDIS_PORT",cast=int,default=6379),
        db=config("REDIS_DB",cast=int,default=0),
        password=config("REDIS_PASSWORD",cast=str)
    )
    logger.info("Successfully connected to redis server")
except Exception as e:
    logger.error("Failed to connect to redis server " + str(e))

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS':{
        "Bearer":{
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
        }
    }
}


REST_FRAMEWORK = {
    "DEFAULT_VERSIONING": "rest_framework.versioning.URLPathVersioning",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        'rest_framework.authentication.TokenAuthentication',
    ],
    "DEFAULT_PERMISSION_CLASSES":[
        "rest_framework.permissions.IsAuthenticated",
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,  # Default number of items per page

    # Filtering settings
    # 'DEFAULT_FILTER_BACKENDS': [
    #     'django_filters.rest_framework.DjangoFilterBackend'
    # ],
}

GUARDIAN_RAISE_403 = True

ACCOUNT_LOGIN_METHODS = {"email","username"}
ACCOUNT_SIGNUP_FIELDS =  ["username*","email*","password1*","password2*"]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "allauth.account.middleware.AccountMiddleware",
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
USE_SQLITE = config("USE_SQLITE",cast=str,default=False)
logger.info("USE_SQLITE: " + str(USE_SQLITE))
if USE_SQLITE:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    logger.error("No database selected")

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
STATIC_ROOT =  BASE_DIR / "staticfiles"

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    "version": 1,
    "disable_existing_logger": False,
    "formatters":{
        "verbose":{
            "format":"{levelname} {asctime} {message}",
            "style": "{"
        },
        "simple":{
            "format":"{levelname} {message}",
            "style": "{"
        }
    },
    "handlers":{
        "console":{
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "simple",
        },
        "file":{
            "class": "logging.FileHandler",
            "level": "WARNING",
            "filename": BASE_DIR / "warnings.log",
            "formatter": "verbose",
        },
    },
    "loggers":{
        "django":{
            "handlers":["console","file"],
            "propagate": True
        }
    }
}