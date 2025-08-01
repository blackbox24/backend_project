from pathlib import Path
from decouple import config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY", cast=str)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", cast=bool)
logger.info(f"DEBUG: {DEBUG}")


ALLOWED_HOSTS = config("ALLOWED_HOSTS").split(",")
logger.info(f"ALLOWED_HOSTS: {ALLOWED_HOSTS}")

# REDIS CONNECTION
try:
    import redis
    r = redis.Redis(
        host = config("REDIS_HOST",cast=str,default="localhost"),
        port = config("REDIS_PORT",cast=int,default=6379),
        password = config("REDIS_PASSWORD",cast=str,default=None),
        db = config("REDIS_DB",cast=int,default=0),
    )
    logger.info("Redis server successfully connected")
except redis.ConnectionError as e:
    logger.error(e)
except:
    logger.error("Failed to connect to redis server")
    raise

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
    "rest_framework",
    "drf_yasg",
]

CUSTOM_APPS = [
    "blog",
]

INSTALLED_APPS = DEFAULT_APPS + THIRD_PARTY_APPS + CUSTOM_APPS

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
USE_SQLITE = config("USE_SQLITE", cast=bool)
logger.info("USE_SQLITE: "+ str(USE_SQLITE))

if USE_SQLITE:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config("SQL_DATABASE", cast=str),
            "USER": config("SQL_USER", cast=str),
            "HOST": config("SQL_HOST", cast=str),
            "PORT": config("SQL_PORT", cast=str),
            "PASSWORD": config("SQL_PASSWORD", cast=str),
        }
    }


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

REST_FRAMEWORK = {
    "DEFAULT_VERSION_CLASSES":"rest_framework.versioning.URLPathVersioning",
}

CACHES = {
    "default":{
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{config("REDIS_HOST")}:{config("REDIS_PORT")}/{config("REDIS_DB")}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "api_key":{
            "type":"apiKey",
            "name": "Authorization",
            "in": "header"
        }
    }
}
# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/


STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    "version": 1,
    "diable_existing_logger": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{"
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "file": {
            "level": "WARNING",
            "class": "logging.FileHandler",
            "formatter": "verbose",
            "filename": BASE_DIR / "warnings.log",
        }
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "propagate": True
        }
    }
}
