from django.db import models

from .platforms.wallex import Wallex
from reusable.models import BaseModel


class Exchange(BaseModel):
    WALLEX = 'wallex'
    NAME_CHOICES = ((WALLEX, WALLEX),)
    name = models.CharField(max_length=100, choices=NAME_CHOICES)

    def get_platform(self):
        if self.name == Exchange.WALLEX:
            return Wallex()

    def tether_price(self, market):
        return self.get_platform().get_price(market)


class Market(BaseModel):
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)

    def __str__(self) -> str:
        return f"<{self.pk} - {self.code}>"

    @property
    def price(self):
        pass
