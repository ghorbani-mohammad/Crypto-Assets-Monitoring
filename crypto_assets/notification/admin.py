from django.contrib import admin

from reusable.admins import ReadOnlyAdminDateFieldsMIXIN

from . import models


@admin.register(models.Notification)
class NotificationAdmin(ReadOnlyAdminDateFieldsMIXIN, admin.ModelAdmin):
    readonly_fields = ("last_sent",)
    raw_id_fields = ("transaction",)
    list_display = (
        "pk",
        "coin",
        "transaction",
        "get_price",
        "percentage",
        "market",
        "profile",
        "status",
        "last_sent",
        "interval",
    )
    list_filter = ("coin",)

    @admin.display(description="price")
    def get_price(self, instance):
        if instance.price:
            return f"{float(instance.price):,}"
