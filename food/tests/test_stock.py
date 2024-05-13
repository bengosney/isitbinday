# Standard Library

# Django

# Locals
from ..models import Location, Stock
from .base import BaseTestCase


class StockTestCase(BaseTestCase):
    def test_transfer_all(self):
        stock = self.product.transfer_in(self.user, quantity=10)
        secondLocation, _ = Location.objects.get_or_create(name="Second")
        newStock, stockLeft = stock.transfer(secondLocation)

        self.assertIsNone(stockLeft)
        self.assertEqual(newStock.quantity, 10)
        self.assertEqual(stock.product, newStock.product)
        self.assertEqual(stock.expires, newStock.expires)

        self.assertEqual(stock.state, Stock.STATE_TRANSFERRED)
        self.assertNotEqual(newStock.state, Stock.STATE_TRANSFERRED)

    def test_transfer_some(self):
        stock = self.product.transfer_in(self.user, quantity=10)
        secondLocation, _ = Location.objects.get_or_create(name="Second")
        newStock, stockLeft = stock.transfer(secondLocation, quantity=5)

        self.assertEqual(stockLeft.quantity, 5)
        self.assertEqual(newStock.quantity, 5)
        self.assertEqual(stock.product, newStock.product)
        self.assertEqual(stock.expires, newStock.expires)
        self.assertEqual(stock.state, Stock.STATE_TRANSFERRED)

    def test_consume_all(self, quantity=10):
        stock = self.product.transfer_in(self.user, quantity=quantity)

        stockLeft = stock.consume()
        self.assertEqual(stock.quantity, 10)
        self.assertIsNone(stockLeft)

    def test_consume_some(self, quantity=10):
        toConsume = quantity // 2
        stock = self.product.transfer_in(self.user, quantity=quantity)

        stockLeft = stock.consume(toConsume)
        self.assertEqual(stock.quantity, toConsume)
        self.assertEqual(stockLeft.quantity, quantity - toConsume)

    def test_remove_all(self, quantity=10):
        stock = self.product.transfer_in(self.user, quantity=quantity)

        stockLeft = stock.remove()
        self.assertEqual(stock.quantity, 10)
        self.assertIsNone(stockLeft)

    def test_remove_some(self, quantity=10):
        toConsume = quantity // 2
        stock = self.product.transfer_in(self.user, quantity=quantity)

        stockLeft = stock.remove(toConsume)
        self.assertEqual(stock.quantity, toConsume)
        self.assertEqual(stockLeft.quantity, quantity - toConsume)
