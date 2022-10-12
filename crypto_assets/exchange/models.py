from django.db import models
from django_jalali.db import models as jmodels
from django.utils.functional import cached_property

from user.models import Profile
from .platforms.bitpin import Bitpin
from .platforms.wallex import Wallex
from reusable.models import BaseModel


class Exchange(BaseModel):
    WALLEX = "wallex"
    BITPIN = "bitpin"
    NAME_CHOICES = ((WALLEX, WALLEX), (BITPIN, BITPIN))
    name = models.CharField(max_length=100, choices=NAME_CHOICES)

    def __str__(self):
        return f"({self.pk} - {self.name})"

    def get_platform(self):
        if self.name == Exchange.WALLEX:
            return Wallex()
        elif self.name == Exchange.BITPIN:
            return Bitpin()

    def price(self, coin, market):
        return self.get_platform().get_price(coin, market)

    def cache_all_prices(self):
        return self.get_platform().cache_all_prices()


class Coin(BaseModel):
    code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"({self.pk} - {self.code})"

    def get_price(self, market):
        if market == Transaction.TOMAN:
            number = int(self.price(market))
            return "{:,}".format(number)
        return float(round(self.price(market), 2))

    def price(self, market):
        exchange = Exchange.objects.last()
        return exchange.price(self, market)


class Transaction(BaseModel):
    BUY = "buy"
    SELL = "sell"
    TYPE_CHOICES = ((BUY, BUY), (SELL, SELL))
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    TOMAN = "toman"
    TETHER = "tether"
    MARKET_CHOICES = ((TOMAN, TOMAN), (TETHER, TETHER))
    jdate = jmodels.jDateField(null=True, blank=True)
    price = models.DecimalField(max_digits=20, decimal_places=10)
    quantity = models.DecimalField(max_digits=20, decimal_places=10)
    market = models.CharField(max_length=10, choices=MARKET_CHOICES, null=True)
    coin = models.ForeignKey(
        Coin, related_name="transactions", on_delete=models.CASCADE
    )
    profile = models.ForeignKey(
        Profile, related_name="transactions", on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return f"({self.pk} - {self.type} - {self.coin})"

    @property
    def total_price(self):
        return int(self.price * self.quantity)

    @cached_property
    def get_current_value(self):
        return int(self.coin.price(self.market) * self.quantity)

    @property
    def get_price(self):
        if self.market == Transaction.TOMAN:
            number = int(self.price)
            return "{:,}".format(number)
        return float(round(self.price, 2))

    @property
    def get_current_price(self):
        if self.market == Transaction.TOMAN:
            number = int(self.coin.price(self.market))
            return "{:,}".format(number)
        return float(round(self.coin.price(self.market), 2))

    @property
    def get_quantity(self):
        return float(round(self.quantity, 6))

    @property
    def get_profit_or_loss(self):
        number = int(self.get_current_value - self.total_price)
        return "{:,}".format(number)

    @property
    def get_total_price(self):
        return "{:,}".format(self.total_price)

    @property
    def get_current_value_admin(self):
        return "{:,}".format(self.get_current_value)
