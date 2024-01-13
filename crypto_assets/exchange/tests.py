from django.test import TestCase
from django.core.cache import cache

from .platforms.bitpin import Bitpin


class BitpinTestCase(TestCase):
    def setUp(self):
        cache.clear()

    def tearDown(self):
        cache.clear()

    # write unittest for bitpin prices
    def test_bitpin_prices(self):
        print("**** test_bitpin_prices ****")
        # bitpin = Bitpin()
        # bitpin.cache_all_prices()
        # assert cache.get("coin_btc_irt") > 0
