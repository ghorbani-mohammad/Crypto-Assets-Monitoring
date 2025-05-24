from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r"transactions", views.TransactionViewSet, basename="transaction")

urlpatterns = [
    path("", include(router.urls)),
    path("cached-prices/", views.cached_prices, name="cached_prices"),
]
