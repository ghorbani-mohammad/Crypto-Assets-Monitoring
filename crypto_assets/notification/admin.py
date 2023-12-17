from django.contrib import admin

from reusable.admins import ReadOnlyAdminDateFields

from . import models


@admin.register(models.Notification)
class NotificationAdmin(ReadOnlyAdminDateFields, admin.ModelAdmin):
    readonly_fields = ("last_sent",)
    list_display = (
        "pk",
        "get_price",
        "coin",
        "market",
        "profile",
        "status",
        "last_sent",
        "interval",
    )

    @admin.display(description="price")
    def get_price(self, instance):
        return f"{float(instance.price):,}"
