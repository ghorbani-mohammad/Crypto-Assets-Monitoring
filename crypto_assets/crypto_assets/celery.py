from __future__ import absolute_import

import os
from logging.config import dictConfig

from celery import Celery
from celery.signals import setup_logging
from django.conf import settings


# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crypto_assets.settings")
app = Celery("crypto_assets")

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object("django.conf:settings")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

DEFAULT_QUEUE = "celery"
MINUTE = 60


if not settings.DEBUG:

    @app.task(bind=True)
    def debug_task(self):
        print(f"Request: {self.request!r}")

    @setup_logging.connect
    def config_loggers(*_args, **_kwargs):
        dictConfig(settings.LOGGING)


app.conf.beat_schedule = {
    "update-bitpin-prices-240": {
        "task": "update_bitpin_prices",
        "schedule": MINUTE * 4,
    },
    "check_coin_notifications": {
        "task": "check_coin_notifications",
        "schedule": MINUTE * 15,
    },
    "check_transaction_notifications": {
        "task": "check_transaction_notifications",
        "schedule": MINUTE * 15,
    },
}
