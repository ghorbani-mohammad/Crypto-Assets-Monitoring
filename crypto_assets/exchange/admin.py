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
    list_display = [
        'pk',
        'coin',
        'type',
        'get_quantity',
        'get_price',
        'get_total_price',
        'get_current_price',
        'get_current_value',
        'get_profit_or_loss',
    ]
    list_filter = ['coin']

    @admin.display(description="price")
    def get_price(self, instance):
        return instance.get_price

    @admin.display(description="current price")
    def get_current_price(self, instance):
        return instance.get_current_price

    @admin.display(description="quantity")
    def get_quantity(self, instance):
        return instance.get_quantity

    @admin.display(description="current value")
    def get_current_value(self, instance):
        return instance.get_current_value

    @admin.display(description="profit/loss")
    def get_profit_or_loss(self, instance):
        return instance.get_profit_or_loss
    
    @admin.display(description="total price")
    def get_total_price(self, instance):
        return instance.get_total_price
