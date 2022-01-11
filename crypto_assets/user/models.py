from django.db import models
from django.contrib.auth.models import AbstractUser


class Profile(AbstractUser):
    mobile_number = models.SlugField(max_length=11, null=True, blank=True, unique=True)
