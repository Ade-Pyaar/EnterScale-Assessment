import os
from pathlib import Path
import re
import sys

from environs import Env


env = Env()
env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, os.path.join(BASE_DIR, "apps"))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "313e8357c0dd828e35bed2240d21bdaafe71f080a9370401358d1787349766a6"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


SESSION_COOKIE_SECURE = False

CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_ALL_ORIGINS = True
CSRF_COOKIE_SECURE = False

CORS_URLS_REGEX = r"^/api/.*$"


# the values will have https://
CORS_ALLOWED_ORIGINS = ["http://*"]


# the values will have https://
CSRF_TRUSTED_ORIGINS = ["http://*"]


# Application definition

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "corsheaders",
    "drf_yasg",
    "django_celery_results",
    "django_celery_beat",
]


SELF_APPS = ["apps.core", "apps.customer", "apps.vendor"]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + SELF_APPS

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "apps.core.middlewares.Log500ErrorsMiddleware",
    "djangorestframework_camel_case.middleware.CamelCaseMiddleWare",
]

ROOT_URLCONF = "FoodOrdering.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "FoodOrdering.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/


LANGUAGE_CODE = "en-us"

TIME_ZONE = "Africa/Lagos"

USE_I18N = False

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = (os.path.join(BASE_DIR, "staticfiles"),)

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"  # new


# MEDIA Folder settings
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# overriding user model
AUTH_USER_MODEL = "core.CustomUser"


# overriding authentication backend
AUTHENTICATION_BACKENDS = ["apps.core.custom_authentication.CustomAuthenticationBackend"]


# setting restframework authentication class
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "apps.core.api_authentication.MyAPIAuthentication",
    ],
    "DEFAULT_RENDERER_CLASSES": (
        "djangorestframework_camel_case.render.CamelCaseJSONRenderer",
        "djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer",
        # Any other renders
    ),
    "DEFAULT_PARSER_CLASSES": (
        # If you use MultiPartFormParser or FormParser, we also have a camel case version
        "djangorestframework_camel_case.parser.CamelCaseFormParser",
        "djangorestframework_camel_case.parser.CamelCaseMultiPartParser",
        "djangorestframework_camel_case.parser.CamelCaseJSONParser",
        # Any other parsers
    ),
}


# settings for swagger documentation
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {"Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}},
    "PERSIST_AUTH": True,
    "USE_SESSION_AUTH": False,
    "DEFAULT_MODEL_RENDERING": "example",
}


if DEBUG:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] -> %(message)s",
                "datefmt": "%d/%b/%Y %H:%M:%S",
            },
        },
        "handlers": {
            "server": {
                "level": "DEBUG",
                "class": "logging.FileHandler",
                "filename": "logs/server_debug.log",
                "formatter": "standard",
            },
            "console": {
                "level": "INFO",
                "class": "logging.StreamHandler",
                "formatter": "standard",
            },
            # apps logger handlers
            "core_handler": {
                "level": "DEBUG",
                "class": "logging.FileHandler",
                "filename": "logs/core.log",
                "formatter": "standard",
            },
            "items_handler": {
                "level": "DEBUG",
                "class": "logging.FileHandler",
                "filename": "logs/items.log",
                "formatter": "standard",
            },
            "business_handler": {
                "level": "DEBUG",
                "class": "logging.FileHandler",
                "filename": "logs/business.log",
                "formatter": "standard",
            },
            "sales_handler": {
                "level": "DEBUG",
                "class": "logging.FileHandler",
                "filename": "logs/sales.log",
                "formatter": "standard",
            },
        },
        "loggers": {
            "django.server": {
                "handlers": ["server", "console"],
                "level": "DEBUG",
                "propagate": True,
            },
            "server_error": {
                "handlers": ["server", "console"],
                "level": "DEBUG",
                "propagate": True,
            },
            "django": {
                "handlers": ["server", "console"],
                "level": "INFO",
                "propagate": True,
            },
            # apps logger
            "core_logger": {
                "handlers": ["core_handler", "console"],
                "level": "DEBUG",
                "propagate": True,
            },
            "items_logger": {
                "handlers": ["items_handler", "console"],
                "level": "DEBUG",
                "propagate": True,
            },
            "business_logger": {
                "handlers": ["business_handler", "console"],
                "level": "DEBUG",
                "propagate": True,
            },
            "sales_logger": {
                "handlers": ["sales_handler", "console"],
                "level": "DEBUG",
                "propagate": True,
            },
        },
    }


else:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] -> %(message)s",
                "datefmt": "%d/%b/%Y %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "level": "INFO",
                "class": "logging.StreamHandler",
                "formatter": "standard",
            },
        },
        "loggers": {
            "django.server": {
                "handlers": ["console"],
                "level": "DEBUG",
                "propagate": True,
            },
            "server_error": {
                "handlers": ["console"],
                "level": "DEBUG",
                "propagate": True,
            },
            "django": {
                "handlers": ["console"],
                "level": "INFO",
                "propagate": True,
            },
            # apps logger
            "core_logger": {
                "handlers": ["console"],
                "level": "DEBUG",
                "propagate": True,
            },
            "items_logger": {
                "handlers": ["console"],
                "level": "DEBUG",
                "propagate": True,
            },
            "business_logger": {
                "handlers": ["console"],
                "level": "DEBUG",
                "propagate": True,
            },
            "sales_logger": {
                "handlers": ["console"],
                "level": "DEBUG",
                "propagate": True,
            },
        },
    }


IGNORABLE_404_URLS = [
    re.compile(r"^/apple-touch-icon.*\.png$"),
    re.compile(r"^/favicon\.ico$"),
    re.compile(r"^/undefined$"),
    re.compile(r"^/robots\.txt$"),
    re.compile(r"\.(php|cgi)$"),
]


GENERATE_CODE = False
DEFAULT_OTP = "123456"
OTP_EXPIRATION_MINUTES = 5
OTP_GENERATE_TIME_LAPSE_MINUTES = 1
MAX_LOGIN_ATTEMPTS = 4


PAYSTACK_SECRET_KEY = os.environ.get("PAYSTACK_SECRET_KEY")


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
# EMAIL_PORT = 587
EMAIL_PORT = 465
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")


ENVIRONMENT = os.environ.get("ENVIRONMENT", "local")


# REDIS localhost settings
REDIS_HOST = "redis"
REDIS_PORT = "6379"

# Celery Configuration Options
# CELERY_BROKER_URL = 'redis://https://django-email-scheduler.herokuapp.com/:6379'
CELERY_BROKER_TRANSPORT_OPTIONS = {"visibility_timeout": 3600}

# for Heroku
CELERY_BROKER_URL = os.environ.get("REDIS_URL", "redis://" + REDIS_HOST + ":" + REDIS_PORT)
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_SERIALIZER = "json"
CELERY_TIMEZONE = "Africa/Lagos"

# stores your tasks status in django database
# CELERY_RESULT_BACKEND = "django-db"

# Celery beat Setting
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
