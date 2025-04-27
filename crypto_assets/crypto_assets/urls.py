from django.urls import path
from django.contrib import admin


urlpatterns = [path("secret-admin/", admin.site.urls)]

admin.site.index_title = "Crypto Assets"
admin.site.site_title = "Crypto Assets Admin"
admin.site.site_header = "Crypto Assets Administration Panel"
