from __future__ import absolute_import

import os

from celery import Celery
from django.conf import settings
from celery.signals import setup_logging

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
        print("Request: {0!r}".format(self.request))

    @setup_logging.connect
    def config_loggers(*args, **kwags):
        from logging.config import dictConfig
        from django.conf import settings

        dictConfig(settings.LOGGING)


app.conf.beat_schedule = {
    "update-bitpin-prices-30": {
        "task": "update_bitpin_prices",
        "schedule": 30,
    }
}
