from django.contrib import admin

from . import models
from reusable.admins import ReadOnlyAdminDateFields


@admin.register(models.Coin)
class CoinAdmin(ReadOnlyAdminDateFields, admin.ModelAdmin):
    list_display = ['pk', 'code', 'get_current_usdt_price']

    @admin.display(description="usdt price")
    def get_current_usdt_price(self, instance):
        return instance.price('USDT')


@admin.register(models.Exchange)
class ExchangeAdmin(ReadOnlyAdminDateFields, admin.ModelAdmin):
    list_display = ['pk', 'name']


@admin.register(models.Transaction)
class TransactionAdmin(ReadOnlyAdminDateFields, admin.ModelAdmin):
    list_display = ['pk', 'profile', 'coin', 'type', 'price', 'quantity', 'total_price']
