# Django
from django.test import TestCase

# Third Party
import pint

# Locals
from ..models import Ingredient, Unit
from ..serializers import IngredientSerializer


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
        serializer = IngredientSerializer(i)

        self.assertEqual(
            f"{serializer.data['quantity_metric']}",
            f"{i.quantity_base_units.magnitude}",
        )

    def test_serializer_unit(self):
        i = Ingredient(name="flour", unit=Unit(name="oz"), quantity=10.0)
        serializer = IngredientSerializer(i)

        self.assertEqual(
            f"{serializer.data['quantity_metric_unit']}",
            f"{i.quantity_base_units.units}",
        )
