from django.contrib import admin

from . import models
from reusable.admins import ReadOnlyAdminDateFields


@admin.register(models.Coin)
class CoinAdmin(ReadOnlyAdminDateFields, admin.ModelAdmin):
    list_display = ['pk', 'title', 'code']


@admin.register(models.Exchange)
class ExchangeAdmin(ReadOnlyAdminDateFields, admin.ModelAdmin):
    list_display = ['pk', 'name']
