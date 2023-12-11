import os
from pathlib import Path

from envparse import env


DEBUG = env.bool("DEBUG")
SECRET_KEY = env.str("SECRET_KEY")
ALLOWED_HOSTS = ["localhost", "crypto.m-gh.com"]
BASE_DIR = Path(__file__).resolve().parent.parent


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_jalali",
    "user",
    "exchange",
    "notification",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "crypto_assets.urls"

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

WSGI_APPLICATION = "crypto_assets.wsgi.application"

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


USE_TZ = True
USE_I18N = True
USE_L10N = True
TIME_ZONE = "UTC"
LANGUAGE_CODE = "en-us"


STATIC_URL = "/static/"
if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, "static")

if not DEBUG:
    MEDIA_URL = "/static/media/"
else:
    MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "static", "media")


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# CELERY
CELERY_TASK_SERIALIZER = "json"
CELERY_TIMEZONE = "Asia/Tehran"
CELERY_RESULT_SERIALIZER = "json"
CELERY_ACCEPT_CONTENT = ["application/json"]
BROKER_URL = "redis://crypto_assets_redis:6379"
CELERY_RESULT_BACKEND = "redis://crypto_assets_redis:6379"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": env.str("POSTGRES_USERNAME"),
        "PASSWORD": env.str("POSTGRES_PASSWORD"),
        "HOST": "crypto_assets_db",
        "PORT": "5432",
    }
}

AUTH_USER_MODEL = "user.Profile"


# Email Configs
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST = "smtp-mail.outlook.com"
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default=None)
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default=None)

# Email Logging Configs
ADMIN_EMAIL_LOG = env("ADMIN_EMAIL_LOG", default=None)
ADMINS = (("Log Admin", ADMIN_EMAIL_LOG),)
SERVER_EMAIL = EMAIL_HOST_USER

# Logging (Just Email Handler)
if EMAIL_HOST_USER and ADMIN_EMAIL_LOG:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {"format": "%(levelname)s %(message)s"},
        },
        "handlers": {
            "mail_admins": {
                "level": "ERROR",
                "class": "django.utils.log.AdminEmailHandler",
                "formatter": "simple",
            },
        },
        "loggers": {
            # all modules
            "": {
                "level": "ERROR",
                "propagate": False,
                "handlers": ["mail_admins"],
            },
            "celery": {
                "level": "ERROR",
                "propagate": False,
                "handlers": ["mail_admins"],
            },
        },
    }

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


CACHES = {
    "default": {
        "LOCATION": "redis://crypto_assets_redis:6379/10",
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
    }
}
