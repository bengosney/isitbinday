# Standard Library
import random
import string

# Django
from django.contrib.auth.models import User
from django.test import TestCase

# Locals
from .models import Location, Product, Stock


class LocationTestCase(TestCase):
    def test_default_location(self):
        location, _ = Location.objects.get_or_create(name="Kitchen", default=True)
        retrieved = Location.get_default()

        self.assertEquals(location, retrieved)


class ProductCreateTestCase(TestCase):
    def test_create_product(self):
        args = {
            "categories": "Stock Cubes, Stock",
            "code": "5050854977411",
            "name": "Beef Stock Cubes",
            "brand": "ASDA",
            "quantity": "12",
            "unit_of_measure": "Each",
        }
        product = Product.get_or_create(**args)

        self.assertIsInstance(product, Product)
        for key in args:
            prop = getattr(product, key)
            try:
                prop = ", ".join([f"{p.name}" for p in prop.all()])
            except AttributeError:
                pass

            self.assertEqual(f"{prop}", args[key])


class BaseSetupClass:
    def setUp(self) -> None:
        super().setUp()

        self.product = Product.get_or_create("5050854977411", "Beef Stock Cubes", "ASDA", "Stock Cubes", 6, "Each")
        self.location = Location.objects.get_or_create(name="Kitchen", default=True)

        self.password = "".join(random.choice(string.ascii_lowercase) for i in range(12))  # nosec
        self.user: User = User.objects.create_user(username="jacob", email="jacob@example.com", password=self.password)


class ProductTestCase(TestCase, BaseSetupClass):
    def test_transfer_in(self):
        stock = self.product.transfer_in(self.user, quantity=2)
        self.assertIsInstance(stock, Stock)
        self.assertEquals(stock.quantity, 2)


class StockTestCase(TestCase, BaseSetupClass):
    def test_immutable_quantity(self):
        self.assertTrue(False)

    def test_immutable_expiry(self):
        self.assertTrue(False)

    def test_transfer_to(self):
        stock = self.product.transfer_in(self.user, quantity=10)
        secondLocation, _ = Location.objects.get_or_create(name="Second")
        newStock, oldStock = secondLocation.transfer_to(stock)

        self.assertEqual(oldStock.quantity, 0)
        self.assertEqual(newStock.quantity, 10)
        self.assertEqual(oldStock.product, newStock.product)
        self.assertEqual(oldStock.expires, newStock.expires)
