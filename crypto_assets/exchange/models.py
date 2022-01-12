from django.db import models
from django.utils.functional import cached_property

from user.models import Profile
from .platforms.bitpin import Bitpin
from .platforms.wallex import Wallex
from reusable.models import BaseModel


class Exchange(BaseModel):
    WALLEX = 'wallex'
    BITPIN = 'bitpin'
    NAME_CHOICES = ((WALLEX, WALLEX), (BITPIN, BITPIN))
    name = models.CharField(max_length=100, choices=NAME_CHOICES)

    def __str__(self) -> str:
        return self.name

    def get_platform(self):
        if self.name == Exchange.WALLEX:
            return Wallex()
        elif self.name == Exchange.BITPIN:
            return Bitpin()

    def price(self, coin, market):
        return self.get_platform().get_price(coin, market)


class Coin(BaseModel):
    code = models.CharField(max_length=20, unique=True)

    def __str__(self) -> str:
        return self.code

    def price(self, market):
        exchange = Exchange.objects.last()
        return exchange.price(self, market)


class Transaction(BaseModel):
    BUY = 'buy'
    SELL = 'sell'
    TYPE_CHOICES = ((BUY, BUY), (SELL, SELL))
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    TOMAN = 'toman'
    TETHER = 'tether'
    MARKET_CHOICES = ((TOMAN, TOMAN), (TETHER, TETHER))
    market = models.CharField(max_length=10, choices=MARKET_CHOICES, null=True)
    price = models.DecimalField(max_digits=20, decimal_places=10)
    quantity = models.DecimalField(max_digits=20, decimal_places=10)
    coin = models.ForeignKey(
        Coin, related_name='transactions', on_delete=models.CASCADE
    )
    profile = models.ForeignKey(
        Profile, related_name='transactions', on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return f"<{self.pk} - {self.type} - {self.coin}>"

    @property
    def total_price(self):
        return round(self.price * self.quantity, 4)

    @cached_property
    def get_current_value(self):
        return round(self.coin.price(self.market) * self.quantity, 4)

    @property
    def get_price(self):
        return round(self.price, 4)

    @property
    def get_current_price(self):
        return round(self.coin.price(self.market), 4)

    @property
    def get_quantity(self):
        return round(self.quantity, 4)

    @property
    def get_profit_or_loss(self):
        return round((self.get_current_value() - self.total_price), 4)
