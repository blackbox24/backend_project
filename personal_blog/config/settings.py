from pathlib import Path
from decouple import config
from django.core.management.utils import get_random_secret_key
import logging

logging.basicConfig(level=logging.INFO);
logger = logging.getLogger(__name__);

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY",cast=str)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG",cast=bool)
logger.info(f"DEBUG: {DEBUG}")


ALLOWED_HOSTS = config("ALLOWED_HOSTS").split(",")
logger.info(f"ALLOWED_HOSTS: {ALLOWED_HOSTS}")


# Application definition
DEFAULT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    
]

CUSTOM_APPS = [
    "pages",
]

INSTALLED_APPS = DEFAULT_APPS + THIRD_PARTY_APPS + CUSTOM_APPS;

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
        'DIRS': [BASE_DIR / "templates",],
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
logger.info("USE_SQLITE: "+ str(USE_SQLITE));

if USE_SQLITE:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    logger.error("No database found")


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
if config("ENV",cast=str,default="local") == "local":
    STATICFILES_DIRS = [
        BASE_DIR / "static",
    ]

LOGIN_URL = "/account/login";
LOGIN_REDIRECT_URL = "/admin";

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "staticfiles"

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGER = {
    "version": 1,
    "diable_existing_logger":False,
    "formatters":{
        "verbose":{
            "format":"{levelname} {asctime} {message}",
            "style": "{",
        },
        "simple": {
            "format":"{levelname} {message}",
            "style": "{"
        },
    },
    "handlers":{
        "console":{
            "level":"INFO",
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "propagate": True
        },
        "file":{
            "level":"WARNING",
            "class": "FileHandler",
            "formatter": "verbose",
            "propagate": True,
            "filename": BASE_DIR / "warnings.log",
        }
    },
    "loggers":{
        "django":{
            "handlers":["console","file"],
        }
    }
}