from django.contrib import admin

from . import models


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    search_fields = ("username",)
    list_display = (
        "pk",
        "first_name",
        "last_name",
        "mobile_number",
        "username",
    )
