from django.http import JsonResponse
from django.core.cache import cache
from django.conf import settings
import redis

def cached_prices(request):
    """
    API endpoint to get all cached cryptocurrency prices.
    Returns a JSON object with cryptocurrency codes as keys and their prices as values.
    """
    all_prices = {}
    
    # Get connection to Redis
    redis_client = redis.Redis.from_url(settings.CACHES['default']['LOCATION'])
    
    # Get all keys matching the pattern
    coin_keys = redis_client.keys("coin_*")
    
    # Get prices for each key
    for key in coin_keys:
        key_str = key.decode('utf-8')
        parts = key_str.split("_")
        if len(parts) >= 2:
            code = parts[1].lower()
            price = cache.get(key_str)
            if price:
                all_prices[code] = float(price)
    
    return JsonResponse(all_prices) 