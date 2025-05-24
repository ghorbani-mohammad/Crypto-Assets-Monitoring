import json
import logging
from django.http import JsonResponse
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from decimal import Decimal
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from .models import Coin, Transaction
from .serializers import TransactionSerializer

logger = logging.getLogger(__name__)


def format_number(value):
    """
    Format a number to remove trailing zeros.
    If it's a whole number, return an integer, otherwise return a float.
    """
    # Convert to Decimal for precise handling
    if isinstance(value, float) or isinstance(value, int) or isinstance(value, str):
        value = Decimal(str(value))

    # Check if it's a whole number
    if value % 1 == 0:
        return int(value)
    else:
        # Convert to string, remove trailing zeros, convert back to float
        return float(
            str(value).rstrip("0").rstrip(".") if "." in str(value) else str(value)
        )


def cached_prices(request):
    """
    API endpoint to get all cached cryptocurrency prices.
    Returns a JSON object with cryptocurrency codes as keys and their prices as values.
    """
    all_prices = {}

    # Get all coins from the database
    coins = Coin.objects.all()
    logger.info(f"Found {coins.count()} coins in database")

    # Check for cached prices for each coin
    for coin in coins:
        logger.info(f"Checking prices for coin: {coin.code}")
        # Check for direct coin price (format used by Bitpin.cache_all_prices)
        key = f"coin_{coin.code}".lower()
        price = cache.get(key)
        logger.info(f"Checking key: {key}, found price: {price}")

        if price:
            all_prices[coin.code.lower()] = format_number(price)
            logger.info(f"Added price for {coin.code}: {price}")
            continue

        # If not found, check for market-specific keys (format used by update_bitpin_prices task)
        for market in ["irt", "usdt"]:
            key = f"coin_{coin.code}_{market}".lower()
            price = cache.get(key)
            logger.info(f"Checking market key: {key}, found price: {price}")

            if price:
                all_prices[coin.code.lower()] = format_number(price)
                logger.info(f"Added market price for {coin.code}: {price}")
                break

    # If no prices found, try to get any cached values
    if not all_prices:
        logger.warning("No prices found in cache. Checking for any cached values...")
        # Try to get a sample of cached values to see what's in there
        sample_keys = [
            "coin_btc",
            "coin_eth",
            "coin_btc_irt",
            "coin_btc_usdt",
            "coin_eth_irt",
            "coin_eth_usdt",
        ]
        for key in sample_keys:
            value = cache.get(key)
            logger.info(f"Sample key {key}: {value}")

    logger.info(f"Final prices: {all_prices}")
    return JsonResponse(all_prices)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A viewset for viewing transactions.
    """

    serializer_class = TransactionSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Transaction.objects.all().select_related("coin").order_by("-jdate")
