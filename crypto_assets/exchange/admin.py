from django.contrib import admin

from . import models


@admin.register(models.Coin)
class CoinAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'code']


@admin.register(models.Exchange)
class ExchangeAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name']
