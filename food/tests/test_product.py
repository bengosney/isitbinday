# Standard Library
import random
import string

# First Party
from food.models import Product, Stock

# Locals
from .base import BaseTestCase


class ProductTestCase(BaseTestCase):
    def test_transfer_in(self):
        stock = self.product.transfer_in(self.user, quantity=2)
        self.assertIsInstance(stock, Stock)
        self.assertEquals(stock.quantity, 2)

    def test_create_product(self):
        args = {
            "categories": "Stock Cubes, Stock",
            "code": "".join(random.choice(string.digits) for i in range(13)),
            "name": "Beef Stock Cubes",
            "brand": "ASDA",
            "quantity": "12",
            "unit_of_measure": "Each",
        }
        product = Product.get_or_create(**args)

        self.assertIsInstance(product, Product)
        for key, value in args.items():
            prop = getattr(product, key)
            try:
                prop = ", ".join(f"{p.name}" for p in prop.all())
            except AttributeError:
                pass

            self.assertEqual(f"{key}: {prop}", f'{key}: {value}')
