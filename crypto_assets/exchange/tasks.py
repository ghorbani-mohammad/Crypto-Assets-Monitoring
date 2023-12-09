from crypto_assets.celery import app

from exchange.platforms.bitpin import Bitpin


@app.task(name="update_bitpin_prices")
def update_bitpin_prices():
    bitpin = Bitpin()
    bitpin.cache_all_prices(ttl=30)