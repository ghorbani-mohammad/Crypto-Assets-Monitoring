from django.http import JsonResponse
from django.core.cache import cache
from .models import Coin
import json
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (float, Decimal)):
            # Convert to string with no trailing zeros, then back to float
            return float(f"{obj:.10f}".rstrip('0').rstrip('.'))
        return super().default(obj)

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
            all_prices[coin.code.lower()] = float(price)
            logger.info(f"Added price for {coin.code}: {price}")
            continue
            
        # If not found, check for market-specific keys (format used by update_bitpin_prices task)
        for market in ["irt", "usdt"]:
            key = f"coin_{coin.code}_{market}".lower()
            price = cache.get(key)
            logger.info(f"Checking market key: {key}, found price: {price}")
            
            if price:
                all_prices[coin.code.lower()] = float(price)
                logger.info(f"Added market price for {coin.code}: {price}")
                break
    
    # If no prices found, try to get any cached values
    if not all_prices:
        logger.warning("No prices found in cache. Checking for any cached values...")
        # Try to get a sample of cached values to see what's in there
        sample_keys = [
            "coin_btc", "coin_eth",  # Format used by Bitpin.cache_all_prices
            "coin_btc_irt", "coin_btc_usdt", "coin_eth_irt", "coin_eth_usdt"  # Format used by update_bitpin_prices
        ]
        for key in sample_keys:
            value = cache.get(key)
            logger.info(f"Sample key {key}: {value}")
    
    logger.info(f"Final prices: {all_prices}")
    return JsonResponse(all_prices, encoder=CustomJSONEncoder) 