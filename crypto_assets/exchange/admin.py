from django.contrib import admin

from reusable.admins import ReadOnlyAdminDateFieldsMIXIN

from . import models


@admin.register(models.Coin)
class CoinAdmin(ReadOnlyAdminDateFieldsMIXIN, admin.ModelAdmin):
    list_display = (
        "pk",
        "code",
        "market",
        "get_current_usdt_price",
        "get_current_irt_price",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        exchange = models.Exchange.objects.last()
        if exchange:
            exchange.cache_all_prices()

    @admin.display(description="usdt price")
    def get_current_usdt_price(self, instance):
        return instance.get_price("usdt")

    @admin.display(description="toman price")
    def get_current_irt_price(self, instance):
        return instance.get_price("irt")


@admin.register(models.Exchange)
class ExchangeAdmin(ReadOnlyAdminDateFieldsMIXIN, admin.ModelAdmin):
    list_display = ("pk", "name")


@admin.register(models.Transaction)
class TransactionAdmin(ReadOnlyAdminDateFieldsMIXIN, admin.ModelAdmin):
    list_filter = ("coin", "market")
    list_display = (
        "pk",
        "coin",
        "market",
        "type",
        "get_date",
        "get_price",
        "get_quantity",
        "get_total_price",
        "get_current_price",
        "get_current_value",
        "get_profit_or_loss",
        "get_change_percentage",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        exchange = models.Exchange.objects.last()
        if exchange:
            exchange.cache_all_prices()

    def get_ordering(self, request):
        return ["-jdate"]

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
        return instance.get_current_value_admin

    @admin.display(description="profit/loss")
    def get_profit_or_loss(self, instance):
        return instance.get_profit_or_loss

    @admin.display(description="total price")
    def get_total_price(self, instance):
        return instance.get_total_price

    @admin.display(description="date", ordering="jdate")
    def get_date(self, instance):
        return instance.jdate


@admin.register(models.Importer)
class ImporterAdmin(ReadOnlyAdminDateFieldsMIXIN, admin.ModelAdmin):
    list_display = ("pk", "file", "profile", "success_count", "fail_count")
