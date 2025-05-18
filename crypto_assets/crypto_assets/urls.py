from django.urls import path, include
from django.contrib import admin


urlpatterns = [
    path("secret-admin/", admin.site.urls),
    path("api/v1/exc/", include("exchange.urls")),
]

admin.site.index_title = "Crypto Assets"
admin.site.site_title = "Crypto Assets Admin"
admin.site.site_header = "Crypto Assets Administration Panel"
