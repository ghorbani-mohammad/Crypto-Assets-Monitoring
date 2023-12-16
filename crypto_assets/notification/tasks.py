from celery.utils.log import get_task_logger
from django.conf import settings
from django.db.models import Q
from datetime import datetime

from crypto_assets.celery import app
from . import models, utils

logger = get_task_logger(__name__)


@app.task(name="check_coin_notifications")
def check_coin_notifications():
    # This task will check all notifications and send a telegram message,
    #  if the price is reached
    # User can set a notification for a coin's price and market
    #  and if the target hit, a telegram message will be sent
    # User should define when the notification should be sent, at
    #   upper or lower price
    TELEGRAM_BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN
    prices = utils.get_coin_cached_prices()
    if not prices:
        return

    notifications = models.Notification.objects.filter(~Q(status=None))
    for notification in notifications:
        coin_key = f"{notification.coin.code}_{notification.market}".lower()
        tg_account = notification.profile.telegram_account.chat_id
        if not tg_account:
            continue

        price = prices.get(coin_key)
        if price is None:
            continue

        price_repr = f"{float(price):,}"
        message = f"{notification.coin.code} is now {price_repr} {notification.market}"

        if (
            price > notification.price
            and notification.status == models.Notification.UPPER
        ):
            if notification.interval:
                if not notification.passed_interval:
                    continue
            else:
                notification.status = None
            notification.last_sent = datetime.now()
            notification.save()
            utils.send_telegram_message(TELEGRAM_BOT_TOKEN, tg_account, message)
        if (
            price < notification.price
            and notification.status == models.Notification.LOWER
        ):
            if notification.interval:
                if not notification.passed_interval:
                    continue
            else:
                notification.status = None
            notification.last_sent = datetime.now()
            notification.save()
            utils.send_telegram_message(TELEGRAM_BOT_TOKEN, tg_account, message)


@app.task(name="check_transaction_notifications")
def check_transaction_notifications():
    pass
