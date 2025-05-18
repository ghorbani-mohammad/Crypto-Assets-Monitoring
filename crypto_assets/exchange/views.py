from django.http import JsonResponse
from django.core.cache import cache

def cached_prices(request):
    """
    API endpoint to get all cached cryptocurrency prices.
    Returns a JSON object with cryptocurrency codes as keys and their prices as values.
    """
    # Get all keys from cache that start with "coin_"
    all_prices = {}
    
    # Get all coins from cache
    for key in cache.keys("coin_*"):
        # Key format is "coin_{code}_{market}" or "coin_{code}"
        parts = key.split("_")
        if len(parts) >= 2:
            code = parts[1].lower()
            price = cache.get(key)
            if price:
                all_prices[code] = float(price)
    
    return JsonResponse(all_prices) 