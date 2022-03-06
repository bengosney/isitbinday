# Standard Library
import random
import string
from abc import ABC

# Django
from django.contrib.auth.models import User
from django.test import TestCase

# Third Party
from rest_framework.test import APITestCase

# First Party
from food.models import Location, Product


class BaseTestCase(ABC, TestCase):
    def setUp(self) -> None:
        super().setUp()

        self.product = Product.get_or_create("5050854977411", "Beef Stock Cubes", "ASDA", "Stock Cubes", 6, "Each")
        self.location = Location.objects.get_or_create(name="Kitchen", default=True)

        self.password = "".join(random.choice(string.ascii_lowercase) for _ in range(12))

        self.user: User = User.objects.create_user(username="jacob", email="jacob@example.com", password=self.password)


class APIBaseTestCase(ABC, APITestCase):
    def setUp(self):
        self.password = "".join(random.choice(string.ascii_lowercase) for _ in range(12))

        self.user = User.objects.create_user(username="jacob", email="jacob@example.com", password=self.password)
        self.product = Product.get_or_create("5000354904790", "Gravy Granules", "Bisto", "Gravy", 170, "g")
        self.pack = Product.get_or_create("5050854977411", "Beef Stock Cubes", "ASDA", "Stock Cubes", 6, "Each", True)

    def login(self):
        self.client.login(username=self.user.username, password=self.password)
