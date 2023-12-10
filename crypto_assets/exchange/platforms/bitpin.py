import logging
from decimal import Decimal
import requests
from django.core.cache import cache

from .base import BaseExchange


logger = logging.getLogger(__name__)


class Bitpin(BaseExchange):
    def __init__(self):
        self.api_addr = "https://api.bitpin.ir/v1/mkt/markets/"

    def get_price(self, coin, market: str) -> Decimal:
        market = self.market_mapper(market)
        coin_key = f"{coin.code}_{market}"
        cache_price = cache.get(coin_key)
        if cache_price:
            return cache_price
        try:
            coins = requests.get(self.api_addr, timeout=10).json()["results"]
            for item in coins:
                if item["code"] != coin_key:
                    continue
                price = round(Decimal(item["price"]), 2)
                cache.set(coin_key, price, 60)
                return price
        except Exception as e:
            logger.error(e)
            return None

    def cache_all_prices(self, ttl=60):
        coins = requests.get(self.api_addr, timeout=10).json()["results"]
        for coin in coins:
            price = round(Decimal(coin["price"]), 2)
            cache.set(coin["code"], price, ttl)

    def market_mapper(self, market: str):
        if market == "tether":
            return "USDT"
        if market == "toman":
            return "IRT"
        return market
