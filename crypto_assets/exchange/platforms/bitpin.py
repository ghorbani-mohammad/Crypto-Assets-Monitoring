import logging
import decimal
import requests
from django.core.cache import cache

from .base import BaseExchange


logger = logging.getLogger(__name__)


class Bitpin(BaseExchange):
    def __init__(self):
        self.api_addr = "https://api.bitpin.ir/v1/mkt/markets/"

    def get_price(self, coin: str, market: str):
        market = self.market_mapper(market)
        coin_key = f"{coin}_{market}"
        if cache.get(coin_key):
            return cache.get(coin_key)
        try:
            coins = requests.get(self.api_addr).json()["results"]
            for item in coins:
                if item["code"] != coin_key:
                    continue
                price = round(decimal.Decimal(item["price"]), 2)
                cache.set(coin_key, price, 2)
                return price
        except Exception as e:
            logger.error(e)
            return None

    def cache_all_prices(self, ttl=2):
        coins = requests.get(self.api_addr).json()["results"]
        for coin in coins:
            price = round(decimal.Decimal(coin["price"]), 2)
            cache.set(coin["code"], price, ttl)

    def market_mapper(self, market: str):
        if market == "tether":
            return "USDT"
        elif market == "toman":
            return "IRT"
        return market
