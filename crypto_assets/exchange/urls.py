from django.urls import path
from . import views

urlpatterns = [
    path('cached-prices/', views.cached_prices, name='cached_prices'),
] 