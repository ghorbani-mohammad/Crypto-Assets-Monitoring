from django.http import JsonResponse
from django.core.cache import cache
from .models import Coin
import json
from decimal import Decimal

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
    
    # Check for cached prices for each coin
    for coin in coins:
        # Check for both market types
        for market in ["irt", "usdt"]:
            # Format key the same way as in platforms/bitpin.py
            key = f"coin_{coin.code}_{market}".lower()
            price = cache.get(key)
            
            if price:
                all_prices[coin.code.lower()] = float(price)
                # Once we have a price for a coin, we can move to the next coin
                break
                
        # Also check for direct coin price without market suffix
        if coin.code.lower() not in all_prices:
            key = f"coin_{coin.code}".lower()
            price = cache.get(key)
            if price:
                all_prices[coin.code.lower()] = float(price)
    
    # Use custom JSON encoder to format the response
    return JsonResponse(all_prices, json_dumps_params={'cls': CustomJSONEncoder}) 