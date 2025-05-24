from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r"transactions", views.TransactionViewSet, basename="transaction")
router.register(r"cached-prices", views.CachedPricesViewSet, basename="cached-prices")

urlpatterns = [
    path("", include(router.urls)),
]
