import logging
from decimal import Decimal
import requests
from django.core.cache import cache
from django.conf import settings

from exchange.platforms.base import BaseExchange


logger = logging.getLogger(__name__)


class Bitpin(BaseExchange):
    def __init__(self):
        self.api_addr = "https://api.bitpin.ir/v1/mkt/markets/"
        self.price_round = 5
        self.cache_price_ttl = settings.BITPIN_PRICE_CACHE_TTL

    def get_price(self, coin, market: str) -> Decimal:
        coin_key = f"coin_{coin.code}_{market}".lower()
        cache_price = cache.get(coin_key)
        if cache_price:
            return cache_price
        try:
            coins = requests.get(self.api_addr, timeout=10).json()["results"]
            for item in coins:
                if item["code"].lower() != coin_key:
                    continue
                price = round(Decimal(item["price"]), self.price_round)
                cache.set(coin_key, price, self.cache_price_ttl)
                return price
        except Exception as e:
            logger.error(e)
            return None

    def cache_all_prices(self):
        try:
            resp = requests.get(self.api_addr, timeout=10)
            coins = resp.json()["results"]
        except TimeoutError as e:
            error = f"TimeoutError in getting prices from bitpin: {e}"
            logger.error(error)
            return None
        except Exception as e:
            error = f"Error in getting prices from bitpin: {e}"
            error += f"\n\nresponse: {resp}"
            error += f"\n\nresponse code: {resp.status_code}"
            logger.error(e)
            return None
        for coin in coins:
            price = round(Decimal(coin["price"]), self.price_round)
            cache.set(f"coin_{coin['code']}".lower(), price, self.cache_price_ttl)
