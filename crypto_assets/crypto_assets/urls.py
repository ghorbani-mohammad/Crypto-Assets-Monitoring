from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("secret-admin/", admin.site.urls),
]

admin.site.index_title = "Crypto Assets"
admin.site.site_title = "Crypto Assets Django Admin"
admin.site.site_header = "Crypto Assets Django Administration Panel"
