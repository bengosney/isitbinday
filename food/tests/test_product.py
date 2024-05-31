# Standard Library
import random
import string

# Third Party
import pytest

# Locals
from ..models import Product, Stock


@pytest.mark.django_db
def test_transfer_in(product, user):
    stock = product.transfer_in(user, quantity=2)
    assert isinstance(stock, Stock)
    assert stock.quantity == 2


@pytest.mark.django_db
def test_create_product():
    args = {
        "categories": "Stock Cubes, Stock",
        "code": "".join(random.choice(string.digits) for _ in range(13)),
        "name": "Beef Stock Cubes",
        "brand": "ASDA",
        "quantity": "12",
        "unit_of_measure": "Each",
        "is_pack": True,
    }

    product = Product.get_or_create(**args)

    assert isinstance(product, Product)
    for key, value in args.items():
        prop = getattr(product, key)
        try:
            prop = ", ".join(f"{p.name}" for p in prop.all())
        except AttributeError:
            pass

        assert f"{key}: {prop}" == f"{key}: {value}"
