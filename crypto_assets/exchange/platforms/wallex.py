from .base import BaseExchange


class Wallex(BaseExchange):
    def get_tether_price(self, coin):
        return 100
