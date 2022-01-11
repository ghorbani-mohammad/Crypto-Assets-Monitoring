from django.db import models

from reusable.models import BaseModel


class Coin(BaseModel):
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)

    def __str__(self) -> str:
        return f"<{self.pk} - {self.code}>"


class Exchange(BaseModel):
    WALLEX = 'wallex'
    NAME_CHOICES = ((WALLEX, WALLEX),)
    name = models.CharField(max_length=100, choices=NAME_CHOICES)
