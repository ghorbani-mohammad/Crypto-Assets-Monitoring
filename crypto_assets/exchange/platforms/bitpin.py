import logging
import requests
from .base import BaseExchange


logger = logging.getLogger(__name__)


class Bitpin(BaseExchange):
    def get_price(self, coin, market):
        logger.info(f"Bitpin.get_price({coin}, {market})")
        api_addr = 'https://api.bitpin.ir/v1/mkt/markets/'
        try:
            coins = requests.get(api_addr).json()['results']
            for item in coins:
                if item['code'] == f'{coin}_{market}':
                    return round(float(item['price']), 2)
        except Exception as e:
            logger.error(e)
            return None
