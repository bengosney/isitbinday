# Standard Library
import random
import string

# Django
from django.contrib.auth.models import User
from django.test import TestCase

# First Party
from food.models import Location, Product


class BaseSetupClass(TestCase):
    def setUp(self) -> None:
        super().setUp()

        self.product = Product.get_or_create("5050854977411", "Beef Stock Cubes", "ASDA", "Stock Cubes", 6, "Each")
        self.location = Location.objects.get_or_create(name="Kitchen", default=True)

        self.password = "".join(random.choice(string.ascii_lowercase) for i in range(12))  # nosec
        self.user: User = User.objects.create_user(username="jacob", email="jacob@example.com", password=self.password)
