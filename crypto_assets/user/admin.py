from django.contrib import admin

from . import models


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["pk", "first_name", "last_name", "mobile_number", "username"]
    search_fields = [
        "username",
    ]
