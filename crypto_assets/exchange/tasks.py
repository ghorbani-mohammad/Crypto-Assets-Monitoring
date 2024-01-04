import csv
from decimal import Decimal
from datetime import datetime

from celery import shared_task
from crypto_assets.celery import app
from jdatetime import JalaliToGregorian

from .platforms.bitpin import Bitpin
from . import models


def get_georgina(jdate: str):
    persian_time = jdate.split("-")[0].strip()
    persian_date = jdate.split("-")[1].strip()
    # Split the date and time strings into components
    date_components = list(map(int, persian_date.split("/")))
    time_components = list(map(int, persian_time.split(":")))

    # Convert Persian date to Gregorian date
    gregorian_date = JalaliToGregorian(*date_components)
    gregorian_datetime = datetime(
        gregorian_date.gyear,
        gregorian_date.gmonth,
        gregorian_date.gday,
        time_components[0],
        time_components[1],
    )

    return gregorian_datetime


@app.task(name="update_bitpin_prices")
def update_bitpin_prices():
    bitpin = Bitpin()
    bitpin.cache_all_prices()


@shared_task
def process_importer(importer_id):
    success_counter = 0
    fail_counter = 0
    importer = models.Importer.objects.get(pk=importer_id)
    errors = importer.errors or ""
    with open(importer.file.path, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip the header row

        for row in csv_reader:
            date, market, trade_type, amount, total, price, fee = row
            date = get_georgina(date)
            title = market.split("/")[0].lower()
            market = market.split("/")[1].lower()
            if market == "toman":
                market = "irt"
            if market == "tether":
                market = "usdt"
            try:
                coin = models.Coin.objects.get(title__iexact=title)
                transaction_data = {
                    "coin": coin,
                    "type": trade_type,
                    "quantity": Decimal(amount),
                    "price": Decimal(price),
                    "jdate": date,
                    "profile": importer.profile,
                    "market": market,
                }
                _, created = models.Transaction.objects.update_or_create(
                    platform_id=date, defaults=transaction_data
                )
                if created:
                    success_counter += 1
            except Exception as e:
                errors += f"\n\nerror:{e}\nrow: {row}"
                fail_counter += 1

    models.Importer.objects.filter(pk=importer_id).update(
        errors=errors, success_count=success_counter, fail_count=fail_counter
    )
