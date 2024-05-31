# Third Party
import pytest

# Locals
from ..models import Location, Product


@pytest.fixture
def product():
    return Product.get_or_create("5000354904790", "Gravy Granules", "Bisto", "Gravy", 170, "g")


@pytest.fixture
def location():
    return Location.objects.get_or_create(name="Kitchen", default=True)


@pytest.fixture
def pack():
    return Product.get_or_create("5050854977411", "Beef Stock Cubes", "ASDA", "Stock Cubes", 6, "Each", True)
