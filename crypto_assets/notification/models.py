from django.db import models

from user.models import Profile
from exchange.models import Coin, Transaction
from reusable.models import BaseModel


class Telegram(BaseModel):
    chat_id = models.CharField(max_length=10)
    profile = models.ForeignKey(
        Profile, related_name="telegrams", on_delete=models.CASCADE
    )


class Notification(BaseModel):
    price = models.DecimalField(max_digits=20, decimal_places=10)
    coin = models.ForeignKey(
        Coin, related_name="notifications", on_delete=models.CASCADE
    )
    profile = models.ForeignKey(
        Profile, related_name="notifications", on_delete=models.CASCADE
    )

    STATUS_CHOICES = (("upper", "upper"), ("lower", "lower"))
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, null=True, blank=True
    )

    market = models.CharField(
        max_length=10, choices=Transaction.MARKET_CHOICES, null=True
    )
