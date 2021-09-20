# Standard Library
import inspect
import random
import string
from abc import ABC

# Django
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

# Third Party
import pint
from rest_framework import status
from rest_framework.test import APITestCase

# Locals
from .models import Ingredient, Recipe, Unit
from .serializers import ingredientSerializer


def getInsecurePassword(length):
    return "".join(random.choice(string.ascii_lowercase) for i in range(length))  # nosec


class APITestCaseWithUser(ABC, APITestCase):
    def setUp(self):
        self.password = getInsecurePassword(12)
        self.user = User.objects.create_user(username="jacob", email="jacob@example.com", password=self.password)


class RecipeViewsTestCase(APITestCaseWithUser):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.user.username, password=self.password)

    def createRecipes(self, count):
        url = reverse("recipe-list")

        for i in range(count):
            data = {
                "name": f"{inspect.stack()[1].function} - {i}",
                "time": f"0:{i}0:00",
                "description": "string",
                "link": "http://example.com",
            }
            self.assertEqual(status.HTTP_201_CREATED, self.client.post(url, data, format="json").status_code)

    def test_create(self, data={}):
        url = reverse("recipe-list")
        print(url)
        name = "Test Recipe"
        defaultData = {
            "name": name,
            "time": "00:00:00",
            "description": "string",
            "link": "http://example.com",
        }

        response = self.client.post(url, {**defaultData, **data}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Recipe.objects.count(), 1)
        self.assertEqual(name, Recipe.objects.get(name=name).name)

    def test_list(self):
        url = reverse("recipe-list")
        count = 5

        self.createRecipes(count)

        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Recipe.objects.count(), count)
        self.assertEqual(Recipe.objects.count(), int(response.json()["count"]))

    def test_list_only_mine(self):
        password = getInsecurePassword(12)
        secondUser = User.objects.create_user(username="keith", email="keith@example.com", password=password)

        url = reverse("recipe-list")
        count = 5

        self.createRecipes(count)
        self.client.logout()

        self.client.login(username=secondUser.username, password=password)
        self.createRecipes(count)

        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Recipe.objects.count() - count, int(response.json()["count"]))


class UnitsTestCases(TestCase):
    def test_unit_class(self):
        unit = Unit(name="g")
        self.assertIsInstance(unit.unit_class, pint.Quantity)

    def test_unit_class_type(self):
        unit = Unit(name="g")
        self.assertEqual(unit.unit_class.units, "gram")

    def test_unit_name_with_spaces(self):
        unit = Unit(name="Imperial Pint")

        self.assertIsInstance(unit.unit_class, pint.Quantity)
        self.assertEqual(unit.unit_class.units, "imperial_pint")

    def test_cooking_system(self):
        unit = Unit(name="ml")
        ing = Ingredient(name="water", unit=unit, quantity=300)

        self.assertEqual(ing.quantity_metric_unit, "millilitres")

    def test_invalid_unit(self):
        unit_name = "qwerty"
        unit = Unit(name=unit_name)
        ing = Ingredient(name="stuff", unit=unit, quantity=5)

        self.assertEqual(ing.quantity_metric, 5)
        self.assertEqual(ing.quantity_metric_unit, unit_name)


class IngredientTestCases(TestCase):
    def setUp(self) -> None:
        self.units = [
            (Unit(name="gram"), "gram"),
            (Unit(name="oz"), "ounce"),
        ]

        return super().setUp()

    def test_unit_class(self):
        for u, _ in self.units:
            i = Ingredient(name="flour", unit=u, quantity=300.0)

            self.assertIsInstance(i.quantity_class, pint.Quantity)

    def test_unit_names(self):
        qty = 300.0
        for u, name in self.units:
            i = Ingredient(name="flour", unit=u, quantity=qty)

            self.assertEqual(f"{i.quantity_class}", f"{qty} {name}")

    def test_base_unit(self):
        i = Ingredient(name="flour", unit=Unit(name="oz"), quantity=10.0)
        self.assertAlmostEqual(i.quantity_base_units.magnitude, 283.495, 3)

    def test_metric_quantity(self):
        i = Ingredient(name="flour", unit=Unit(name="oz"), quantity=10.0)
        self.assertAlmostEqual(i.quantity_metric, 283.495, 3)

    def test_metric_unit(self):
        i = Ingredient(name="flour", unit=Unit(name="oz"), quantity=10.0)
        self.assertEqual(i.quantity_metric_unit, "gram")

    def test_serializer_quantity(self):
        i = Ingredient(name="flour", unit=Unit(name="oz"), quantity=10.0)
        serializer = ingredientSerializer(i)

        self.assertEqual(f"{serializer.data['quantity_metric']}", f"{i.quantity_base_units.magnitude}")

    def test_serializer_unit(self):
        i = Ingredient(name="flour", unit=Unit(name="oz"), quantity=10.0)
        serializer = ingredientSerializer(i)

        self.assertEqual(f"{serializer.data['quantity_metric_unit']}", f"{i.quantity_base_units.units}")
