import requests
import redis
import pickle
import logging
import urllib.parse

from django.conf import settings

logger = logging.getLogger(__name__)


def send_telegram_message(token: str, chat_id: str, message: str):
    if settings.DEBUG:
        logger.info("sending telegram message is disabled in DEBUG mode")
        logger.info(f"send_telegram_message: {chat_id}, {message}")
        return

    send_text = (
        "https://api.telegram.org/bot"
        + token
        + "/sendMessage?chat_id="
        + str(chat_id)
        + "&text="
        + urllib.parse.quote(message)
    )
    response = requests.get(send_text, timeout=10)
    return response.json()


def get_coin_cached_prices():
    result = {}
    redis_client = redis.StrictRedis(host="crypto_assets_redis", port=6379, db=10)
    coin_keys = redis_client.keys("*coin_*")
    for coin_key in coin_keys:
        coin_price = pickle.loads(redis_client.get(coin_key))
        coin_key = coin_key.decode().split("coin_")[-1]
        result[coin_key] = coin_price
    return result
