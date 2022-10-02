import logging
import requests
from .base import BaseExchange


logger = logging.getLogger(__name__)


class Wallex(BaseExchange):
    def get_price(self, coin, market):
        logger.info(f"Wallex.get_price({coin}, {market})")
        api_addr = "https://api.wallex.ir/v1/markets"
        try:
            coin = requests.get(api_addr).json()["result"]["symbols"][f"{coin}{market}"]
            return round(float(coin["stats"]["lastPrice"]), 2)
        except:
            return None
