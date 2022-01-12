from django.db import models

from user.models import Profile
from .platforms.wallex import Wallex
from reusable.models import BaseModel


class Exchange(BaseModel):
    WALLEX = 'wallex'
    NAME_CHOICES = ((WALLEX, WALLEX),)
    name = models.CharField(max_length=100, choices=NAME_CHOICES)

    def get_platform(self):
        if self.name == Exchange.WALLEX:
            return Wallex()

    def price(self, market):
        return self.get_platform().get_price(market)


class Coin(BaseModel):
    code = models.CharField(max_length=20, unique=True)

    def __str__(self) -> str:
        return f"<{self.pk} - {self.code}>"

    @property
    def price(self):
        pass


class Transaction(BaseModel):
    BUY = 'buy'
    SELL = 'sell'
    TYPE_CHOICES = ((BUY, BUY), (SELL, SELL))
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
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
