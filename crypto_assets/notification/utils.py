import requests
import redis
import pickle
from django.core.cache import cache


def send_telegram_message(token: str, chat_id: str, message: str):
    send_text = (
        "https://api.telegram.org/bot"
        + token
        + "/sendMessage?chat_id="
        + chat_id
        + "&parse_mode=Markdown&text="
        + message
    )
    response = requests.get(send_text, timeout=10)
    return response.json()


def get_coin_cached_prices():
    result = {}
    redis_client = redis.StrictRedis(host='crypto_assets_redis', port=6379, db=10)
    coin_keys = redis_client.keys('*coin_*')
    for coin_key in coin_keys:
        coin_price = pickle.loads(redis_client.get(coin_key))
        coin_key = coin_key.decode().split("coin_")[-1]
        result[coin_key] = coin_price
    return result