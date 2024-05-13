# Standard Library

# Django

# Locals
from ..models import Location, Stock
from .base import BaseTestCase


class StockTestCase(BaseTestCase):
    def test_transfer_all(self):
        stock = self.product.transfer_in(self.user, quantity=10)
        second_location, _ = Location.objects.get_or_create(name="Second")
        new_stock, stock_left = stock.transfer(second_location)

        self.assertIsNone(stock_left)
        self.assertEqual(new_stock.quantity, 10)
        self.assertEqual(stock.product, new_stock.product)
        self.assertEqual(stock.expires, new_stock.expires)

        self.assertEqual(stock.state, Stock.STATE_TRANSFERRED)
        self.assertNotEqual(new_stock.state, Stock.STATE_TRANSFERRED)

    def test_transfer_some(self):
        stock = self.product.transfer_in(self.user, quantity=10)
        second_location, _ = Location.objects.get_or_create(name="Second")
        new_stock, stock_left = stock.transfer(second_location, quantity=5)

        self.assertEqual(stock_left.quantity, 5)
        self.assertEqual(new_stock.quantity, 5)
        self.assertEqual(stock.product, new_stock.product)
        self.assertEqual(stock.expires, new_stock.expires)
        self.assertEqual(stock.state, Stock.STATE_TRANSFERRED)

    def test_consume_all(self, quantity=10):
        stock = self.product.transfer_in(self.user, quantity=quantity)

        stock_left = stock.consume()
        self.assertEqual(stock.quantity, 10)
        self.assertIsNone(stock_left)

    def test_consume_some(self, quantity=10):
        to_consume = quantity // 2
        stock = self.product.transfer_in(self.user, quantity=quantity)

        stock_left = stock.consume(to_consume)
        self.assertEqual(stock.quantity, to_consume)
        self.assertEqual(stock_left.quantity, quantity - to_consume)

    def test_remove_all(self, quantity=10):
        stock = self.product.transfer_in(self.user, quantity=quantity)

        stock_left = stock.remove()
        self.assertEqual(stock.quantity, 10)
        self.assertIsNone(stock_left)

    def test_remove_some(self, quantity=10):
        to_consume = quantity // 2
        stock = self.product.transfer_in(self.user, quantity=quantity)

        stock_left = stock.remove(to_consume)
        self.assertEqual(stock.quantity, to_consume)
        self.assertEqual(stock_left.quantity, quantity - to_consume)
