import requests
from .base import BaseExchange


class Wallex(BaseExchange):
    def get_price(self, coin):
        api_addr = 'https://api.wallex.ir/v1/markets'
        resp = requests.get(api_addr)
        return 100
