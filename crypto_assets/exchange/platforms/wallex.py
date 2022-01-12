import logging
import requests
from .base import BaseExchange


logger = logging.getLogger(__name__)


class Wallex(BaseExchange):
    def get_price(self, coin, market):
        logger.info(f"Wallex.get_price({coin}, {market})")
        api_addr = 'https://api.wallex.ir/v1/markets'
        resp = requests.get(api_addr).json()
        logger.info(f'Wallex response: {resp}')
        for symbol in resp['result']['symbols']:
            logger.info(symbol)
            if symbol['baseAsset'] == coin.code and symbol['quoteAsset'] == market:
                return symbol['stats']['lastPrice']
        return None
