from datetime import datetime
import pytz

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
        Coin,
        related_name="notifications",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    market = models.CharField(
        max_length=10, choices=Transaction.MARKET_CHOICES, null=True
    )

    profile = models.ForeignKey(
        Profile, related_name="notifications", on_delete=models.CASCADE
    )

    UPPER = "upper"
    LOWER = "lower"
    STATUS_CHOICES = ((UPPER, UPPER), (LOWER, LOWER))
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, null=True, blank=True
    )

    transaction = models.ForeignKey(
        Transaction,
        related_name="notifications",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    last_sent = models.DateTimeField(null=True, blank=True)
    # using 0 to indicate that the notification is not recurring
    interval = models.PositiveIntegerField(
        default=0, null=True, blank=True, help_text="in minutes"
    )

    @property
    def passed_interval(self) -> bool:
        if not self.last_sent:
            return True
        time_diff = datetime.now(pytz.UTC) - self.last_sent
        if time_diff.seconds / 60 > self.interval:
            return True
        return False

    @property
    def is_coin(self) -> bool:
        return bool(self.coin)

    @property
    def is_transaction(self) -> bool:
        return bool(self.transaction)
