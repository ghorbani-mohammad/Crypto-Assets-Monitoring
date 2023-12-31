from django.db import models

from user.models import Profile
from exchange.models import Coin
from reusable.models import BaseModel


class Asset(BaseModel):
    profile = models.ForeignKey(
        Profile, related_name="assets", on_delete=models.CASCADE
    )
    coin = models.ForeignKey(Coin, related_name="assets", on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=20, decimal_places=10)
    value = models.DecimalField(max_digits=10, decimal_places=2, null=True)
