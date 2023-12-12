from celery.utils.log import get_task_logger
from django.conf import settings

from crypto_assets.celery import app
from . import models, utils

logger = get_task_logger(__name__)


@app.task(name="check_notifications")
def check_notifications():
    TELEGRAM_BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN
    notifications = models.Notification.objects.filter(status=True)
    prices = utils.get_coin_cached_prices()
    for notification in notifications:
        # TODO: add the logic for checking the price,
        # then send the message to the user
        pass
        # notification.profile.notifications.first()
        # utils.send_telegram_message(TELEGRAM_BOT_TOKEN, account.chat_id, message)
