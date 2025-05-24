from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register(r"transactions", views.TransactionViewSet, basename="transaction")
router.register(r"cached-prices", views.CachedPricesViewSet, basename="cached-prices")
router.register(r"coins", views.CoinViewSet, basename="coins")

urlpatterns = [
    path("", include(router.urls)),
]
