from django.http import JsonResponse
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Coin, Transaction
import json
import logging
from decimal import Decimal

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
        return float(str(value).rstrip('0').rstrip('.') if '.' in str(value) else str(value))

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
            "coin_btc", "coin_eth",  # Format used by Bitpin.cache_all_prices
            "coin_btc_irt", "coin_btc_usdt", "coin_eth_irt", "coin_eth_usdt"  # Format used by update_bitpin_prices
        ]
        for key in sample_keys:
            value = cache.get(key)
            logger.info(f"Sample key {key}: {value}")
    
    logger.info(f"Final prices: {all_prices}")
    return JsonResponse(all_prices)

def get_transactions(request):
    """
    API endpoint to get the user's transactions with pagination.
    Returns a JSON object with transactions and pagination info.
    """
    # Get transactions
    transactions = Transaction.objects.all().select_related('coin')
    
    # Get page number from request
    page_number = request.GET.get('page', 1)
    items_per_page = 10
    
    # Create paginator
    paginator = Paginator(transactions, items_per_page)
    
    try:
        # Get requested page
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page
        page_obj = paginator.page(paginator.num_pages)
    
    # Format transactions as a list of dictionaries
    transaction_list = []
    for tx in page_obj:
        transaction_list.append({
            'id': tx.id,
            'type': tx.type,
            'market': tx.market,
            'coin': tx.coin.code,
            'price': format_number(tx.price),
            'quantity': format_number(tx.quantity),
            'total_price': format_number(tx.total_price),
            'current_value': format_number(tx.get_current_value),
            'date': tx.jdate.strftime('%Y-%m-%d %H:%M:%S') if tx.jdate else None,
            'change_percentage': format_number(tx.get_change_percentage) if tx.type == Transaction.BUY else None
        })
    
    # Prepare pagination info
    response = {
        'transactions': transaction_list,
        'pagination': {
            'current_page': page_obj.number,
            'total_pages': paginator.num_pages,
            'items_per_page': items_per_page,
            'total_items': paginator.count,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'next_page': page_obj.number + 1 if page_obj.has_next() else None,
            'previous_page': page_obj.number - 1 if page_obj.has_previous() else None,
        }
    }
    
    return JsonResponse(response)