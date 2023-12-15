from celery.utils.log import get_task_logger
from django.conf import settings
from django.db.models import Q

from crypto_assets.celery import app
from . import models, utils

logger = get_task_logger(__name__)


@app.task(name="check_notifications")
def check_notifications():
    TELEGRAM_BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN
    notifications = models.Notification.objects.filter(~Q(status=None))
    prices = utils.get_coin_cached_prices()
    if not prices:
        return
    for notification in notifications:
        coin_key = f"{notification.coin.code}_{notification.market}".lower()
        price = prices.get(coin_key)
        if price is None:
            continue
        if price > notification.price and notification.status == models.Notification.UPPER:
            message = f"{notification.coin.code} is now {price:,} {notification.market}"
            notification.status = None
            notification.save()
            utils.send_telegram_message(TELEGRAM_BOT_TOKEN, 110374168, message)
        if price < notification.price and notification.status == models.Notification.LOWER:
            message = f"{notification.coin.code} is now {price:,} {notification.market}"
            notification.status = None
            notification.save()
            utils.send_telegram_message(TELEGRAM_BOT_TOKEN, 110374168, message)
