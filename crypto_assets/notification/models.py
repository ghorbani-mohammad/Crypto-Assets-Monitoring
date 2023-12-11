from django.db import models

from user.models import Profile
from reusable.models import BaseModel


class Telegram(BaseModel):
    chat_id = models.CharField(max_length=10)
    profile = models.ForeignKey(
        Profile, related_name="telegrams", on_delete=models.CASCADE
    )
