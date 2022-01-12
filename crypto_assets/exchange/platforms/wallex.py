import requests
from .base import BaseExchange


class Wallex(BaseExchange):
    def get_price(self, coin, market):
        api_addr = 'https://api.wallex.ir/v1/markets'
        resp = requests.get(api_addr).json()
        for symbol in resp['result']['symbols']:
            if symbol['baseAsset'] == coin.code and symbol['quoteAsset'] == market:
                return symbol['stats']['lastPrice']
        return None
