# Standard Library
import inspect
from datetime import timedelta

# Django
from django.contrib.auth.models import User
from django.urls import reverse

# Third Party
import pint
import pytest
from rest_framework import status

# Locals
from .models import Ingredient, Recipe, Unit
from .serializers import IngredientSerializer


@pytest.fixture
def create_recipes(authenticated_client):
    def _create_recipes(count, client=None):
        _client = client or authenticated_client
        url = reverse("recipes:recipe-list")

        for i in range(count):
            data = {
                "name": f"{inspect.stack()[1].function} - {i}",
                "time": f"0:{i}0:00",
                "description": "string",
                "link": "http://example.com",
            }
            _client.post(url, data, format="json").status_code

    return _create_recipes


@pytest.mark.django_db
def test_create(authenticated_client):
    url = reverse("recipes:recipe-list")
    name = "Test Recipe"
    default_data = {
        "name": name,
        "time": "00:00:00",
        "description": "string",
        "link": "http://example.com",
    }

    response = authenticated_client.post(url, default_data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert Recipe.objects.count() == 1


@pytest.mark.django_db
def test_list(create_recipes, authenticated_client):
    url = reverse("recipes:recipe-list")

    create_recipes(5)

    response = authenticated_client.get(url, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert Recipe.objects.count() == 5
    assert Recipe.objects.count() == int(response.json()["count"])


@pytest.mark.django_db
def test_list_only_mine(insecure_password, create_recipes, authenticated_client):
    url = reverse("recipes:recipe-list")
    count = 5

    second_user = User.objects.create_user(username="keith", email="keith@example.com", password=insecure_password)
    for i in range(count):
        Recipe.objects.create(
            name=f"Other Recipe {i}",
            time=timedelta(minutes=i),
            description="string",
            link="http://example.com",
            owner=second_user,
        )

    create_recipes(count)

    response = authenticated_client.get(url, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert Recipe.objects.count() - count == int(response.json()["count"])


def test_unit_class():
    unit = Unit(name="g")
    assert isinstance(unit.unit_class, pint.Quantity)


def test_unit_class_type():
    unit = Unit(name="g")
    assert unit.unit_class is not None
    assert unit.unit_class.units == "gram"


def test_unit_name_with_spaces():
    unit = Unit(name="Imperial Pint")
    assert isinstance(unit.unit_class, pint.Quantity)
    assert unit.unit_class.units == "imperial_pint"


def test_cooking_system():
    unit = Unit(name="ml")
    ing = Ingredient(name="water", unit=unit, quantity=300)

    assert ing.quantity_metric_unit == "millilitres"


def test_invalid_unit():
    unit_name = "qwerty"
    unit = Unit(name=unit_name)
    ing = Ingredient(name="stuff", unit=unit, quantity=5)

    assert ing.quantity_metric == 5
    assert ing.quantity_metric_unit == unit_name


@pytest.fixture
def units():
    return [
        (Unit(name="gram"), "gram"),
        (Unit(name="oz"), "ounce"),
    ]


def test_ingredient_unit_class(units):
    for u, _ in units:
        i = Ingredient(name="flour", unit=u, quantity=300.0)
        assert isinstance(i.quantity_class, pint.Quantity)


def test_unit_names(units):
    qty = 300.0
    for u, name in units:
        i = Ingredient(name="flour", unit=u, quantity=qty)

        assert f"{i.quantity_class}" == f"{qty} {name}"


def test_base_unit():
    i = Ingredient(name="flour", unit=Unit(name="oz"), quantity=10.0)
    assert i.quantity_base_units.magnitude == pytest.approx(283.495, 3)


def test_metric_quantity():
    i = Ingredient(name="flour", unit=Unit(name="oz"), quantity=10.0)
    assert i.quantity_metric == pytest.approx(283.495, 3)


def test_metric_unit():
    i = Ingredient(name="flour", unit=Unit(name="oz"), quantity=10.0)
    assert i.quantity_metric_unit == "gram"


def test_serializer_quantity():
    i = Ingredient(name="flour", unit=Unit(name="oz"), quantity=10.0)
    serializer = IngredientSerializer(i)

    assert f"{serializer.data['quantity_metric']}" == f"{i.quantity_base_units.magnitude}"


def test_serializer_unit():
    i = Ingredient(name="flour", unit=Unit(name="oz"), quantity=10.0)
    serializer = IngredientSerializer(i)

    assert f"{serializer.data['quantity_metric_unit']}" == f"{i.quantity_base_units.units}"
