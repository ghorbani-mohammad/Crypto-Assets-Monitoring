import requests
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
    # get all keys
    coins = cache.get("*")
    for coin in coins:
        print(coin)
