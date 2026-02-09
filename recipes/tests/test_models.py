# Third Party
import pint
import pytest

# Locals
from ..models import Ingredient, Unit
from ..serializers import IngredientSerializer


class TestUnits:
    def test_unit_class(self):
        unit = Unit(name="g")
        assert isinstance(unit.unit_class, pint.Quantity)

    def test_unit_class_type(self):
        unit = Unit(name="g")
        assert unit.unit_class.units == "gram"

    def test_unit_name_with_spaces(self):
        unit = Unit(name="Imperial Pint")

        assert isinstance(unit.unit_class, pint.Quantity)
        assert unit.unit_class.units == "imperial_pint"

    def test_cooking_system(self):
        unit = Unit(name="ml")
        ing = Ingredient(name="water", unit=unit, quantity=300)

        assert ing.quantity_metric_unit == "millilitres"

    def test_invalid_unit(self):
        unit_name = "qwerty"
        unit = Unit(name=unit_name)
        ing = Ingredient(name="stuff", unit=unit, quantity=5)

        assert ing.quantity_metric == 5
        assert ing.quantity_metric_unit == unit_name


class TestIngredient:
    @pytest.fixture
    def units(self):
        return [
            (Unit(name="gram"), "gram"),
            (Unit(name="oz"), "ounce"),
        ]

    def test_unit_class(self, units):
        for u, _ in units:
            i = Ingredient(name="flour", unit=u, quantity=300.0)

            assert isinstance(i.quantity_class, pint.Quantity)

    def test_unit_names(self, units):
        qty = 300.0
        for u, name in units:
            i = Ingredient(name="flour", unit=u, quantity=qty)

            assert f"{i.quantity_class}" == f"{qty} {name}"

    def test_base_unit(self):
        i = Ingredient(name="flour", unit=Unit(name="oz"), quantity=10.0)
        assert i.quantity_base_units.magnitude == pytest.approx(283.495, abs=0.001)

    def test_metric_quantity(self):
        i = Ingredient(name="flour", unit=Unit(name="oz"), quantity=10.0)
        assert i.quantity_metric == pytest.approx(283.495, abs=0.001)

    def test_metric_unit(self):
        i = Ingredient(name="flour", unit=Unit(name="oz"), quantity=10.0)
        assert i.quantity_metric_unit == "gram"

    def test_serializer_quantity(self):
        i = Ingredient(name="flour", unit=Unit(name="oz"), quantity=10.0)
        serializer = IngredientSerializer(i)

        assert f"{serializer.data['quantity_metric']}" == f"{i.quantity_base_units.magnitude}"

    def test_serializer_unit(self):
        i = Ingredient(name="flour", unit=Unit(name="oz"), quantity=10.0)
        serializer = IngredientSerializer(i)

        assert f"{serializer.data['quantity_metric_unit']}" == f"{i.quantity_base_units.units}"
