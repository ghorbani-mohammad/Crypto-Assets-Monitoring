from django.contrib import admin

from . import models
from reusable.admins import ReadOnlyAdminDateFieldsMIXIN


@admin.register(models.Asset)
class AssetAdmin(ReadOnlyAdminDateFieldsMIXIN, admin.ModelAdmin):
    readonly_fields = ("quantity", "value")
    list_display = (
        "pk",
        "profile",
        "coin",
        "quantity",
        "get_value",
    )
    list_filter = ("coin",)

    @admin.display(description="value")
    def get_value(self, instance):
        if instance.value:
            return f"{float(instance.value):,}"