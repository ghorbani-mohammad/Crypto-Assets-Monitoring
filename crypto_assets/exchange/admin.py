from django.contrib import admin

from . import models

# Register your models here.
@admin.register(models.Coin)
class CoinAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'code']
