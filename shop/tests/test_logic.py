from django.test import TestCase
from shop.utils import *

class CalculateMoneyDefTestCase(TestCase):

    def test_sum_count_price_pass(self):
        result = sum_price_count(price=100, quantity=10)
        self.assertEquals(1000, result)

    def test_sum_count_price_discount_pass(self):
        result = sum_price_count(price=200, quantity=15, discount=5)
        self.assertEquals(2850, result)

    def test_sum_count_nds_pass(self):
        result = sum_price_count(price=400, quantity=6, nds=7)
        self.assertEquals(2232, result)

    def test_sum_count_nds_discount_pass(self):
        result = sum_price_count(price=500, quantity=105, discount=6, nds=12)
        self.assertEquals(43428, result)


class CalculateMoneyClassTestCase(TestCase, CalculateMoney):
    def test_sum_price_pass(self):
        list_price = [294, 2000, 6942]
        result = self.sum_price(list_price)
        self.assertEquals(9236, result)

    def test_sum_price_count_pass(self):
        result = self.sum_price_count(price=400, quantity=19)
        self.assertEquals(7600, result)
