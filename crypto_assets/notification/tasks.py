from datetime import datetime

from celery.utils.log import get_task_logger
from django.conf import settings
from django.db.models import Q

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
    bot_token = settings.TELEGRAM_BOT_TOKEN
    prices = utils.get_coin_cached_prices()
    if not prices:
        return

    notifications = models.Notification.objects.filter(~Q(status=None))
    for notification in notifications:
        coin_key = f"{notification.coin.code}_{notification.market}".lower()

        tg_account = notification.profile.telegram_account.chat_id
        price = prices.get(coin_key)
        if not tg_account or price is None:
            continue

        price_repr = f"{float(price):,}"
        message = f"{notification.coin.code}: {price_repr} {notification.market}"

        send_message = False

        if (
            price > notification.price
            and notification.status == models.Notification.UPPER
        ):
            message = f"🟢 {message}"
            if notification.interval:
                if not notification.passed_interval:
                    continue
            else:
                notification.status = None
            send_message = True
        if (
            price < notification.price
            and notification.status == models.Notification.LOWER
        ):
            message = f"🔴 {message}"
            if notification.interval:
                if not notification.passed_interval:
                    continue
            else:
                notification.status = None
            send_message = True

        if send_message:
            notification.last_sent = datetime.now()
            notification.save()
            utils.send_telegram_message(bot_token, tg_account, message)


def format_message(transaction, change_percentage):
    """
    Format the message to be sent to the user
    """
    icon = "🟢" if change_percentage >= 0 else "🔴"
    message = f"{icon} #{transaction.pk}"
    message += f"\n\ncoin: {transaction.coin.code} {transaction.market.upper()}"
    message += f"\nquantity: {transaction.quantity}"
    message += f"\nbought price: {transaction.get_price}"
    message += f"\ncurrent price: {transaction.get_current_price}"
    message += f"\n\nprofit/loss percentage: {change_percentage}%"
    message += f"\nprofit/loss value: {transaction.get_profit_or_loss}"
    return message


@app.task(name="check_transaction_notifications")
def check_transaction_notifications():
    notifications = (
        models.Notification.objects.filter(
            transaction__isnull=False, percentage__isnull=False
        )
        .select_related("transaction", "profile")
        .order_by("?")
    )

    for notification in notifications:
        transaction = notification.transaction
        change_percentage = transaction.get_change_percentage
        should_notify = (
            notification.status == models.Notification.UPPER
            and change_percentage >= notification.percentage
        ) or (
            notification.status == models.Notification.LOWER
            and change_percentage <= notification.percentage
        )

        if should_notify:
            message = format_message(transaction, change_percentage)
            utils.send_telegram_message(
                settings.TELEGRAM_BOT_TOKEN,
                notification.profile.telegram_account.chat_id,
                message,
            )
