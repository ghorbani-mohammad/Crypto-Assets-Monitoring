from django.contrib import admin

from . import models
from reusable.admins import ReadOnlyAdminDateFieldsMIXIN


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    search_fields = ("username",)
    list_display = ("pk", "username", "last_name", "first_name", "mobile_number")


@admin.register(models.TelegramAccount)
class TelegramAccountAdmin(admin.ModelAdmin):
    list_display = ("pk", "profile", "chat_id")


@admin.register(models.Channel)
class ChannelAdmin(ReadOnlyAdminDateFieldsMIXIN):
    list_display = ("pk", "name", "description")
