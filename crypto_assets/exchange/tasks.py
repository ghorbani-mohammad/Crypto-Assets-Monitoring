from crypto_assets.celery import app

from .platforms.bitpin import Bitpin
from . import models


@app.task(name="update_bitpin_prices")
def update_bitpin_prices():
    bitpin = Bitpin()
    bitpin.cache_all_prices()


# a task should run after creating Importer object
# it should read the file and create transactions
@app.task(name="process_importer")
def process_importer(importer_id):
    importer = models.Importer.objects.get(pk=importer_id)
    importer.process()
