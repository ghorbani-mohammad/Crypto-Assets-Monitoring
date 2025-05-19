from django.http import JsonResponse
from django.core.cache import cache
from .models import Coin

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
                # Format float to remove trailing zeros
                formatted_price = float(f"{float(price):g}")
                all_prices[coin.code.lower()] = formatted_price
                # Once we have a price for a coin, we can move to the next coin
                break
                
        # Also check for direct coin price without market suffix
        if coin.code.lower() not in all_prices:
            key = f"coin_{coin.code}".lower()
            price = cache.get(key)
            if price:
                # Format float to remove trailing zeros
                formatted_price = float(f"{float(price):g}")
                all_prices[coin.code.lower()] = formatted_price
    
    return JsonResponse(all_prices) 