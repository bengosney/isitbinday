# Third Party
import pytest

# Locals
from ..models import Location, Stock


@pytest.mark.django_db
def test_transfer_all(product, user):
    stock = product.transfer_in(user, quantity=10)
    second_location, _ = Location.objects.get_or_create(name="Second")
    new_stock, stock_left = stock.transfer(second_location)

    assert stock_left is None
    assert new_stock.quantity == 10
    assert stock.product == new_stock.product
    assert stock.expires == new_stock.expires

    assert stock.state == Stock.STATE_TRANSFERRED
    assert new_stock.state != Stock.STATE_TRANSFERRED


@pytest.mark.django_db
def test_transfer_some(product, user):
    stock = product.transfer_in(user, quantity=10)
    second_location, _ = Location.objects.get_or_create(name="Second")
    new_stock, stock_left = stock.transfer(second_location, quantity=5)

    assert stock_left.quantity == 5
    assert new_stock.quantity == 5
    assert stock.product == new_stock.product
    assert stock.expires == new_stock.expires
    assert stock.state == Stock.STATE_TRANSFERRED


@pytest.mark.django_db
def test_consume_all(product, user):
    quantity = 10
    stock = product.transfer_in(user, quantity=quantity)

    stock_left = stock.consume()
    assert stock.quantity == 10
    assert stock_left is None


@pytest.mark.django_db
def test_consume_some(product, user):
    quantity = 10
    to_consume = quantity // 2
    stock = product.transfer_in(user, quantity=quantity)

    stock_left = stock.consume(to_consume)
    assert stock.quantity == to_consume
    assert stock_left.quantity == quantity - to_consume


@pytest.mark.django_db
def test_remove_all(product, user):
    quantity = 10
    stock = product.transfer_in(user, quantity=quantity)

    stock_left = stock.remove()
    assert stock.quantity == 10
    assert stock_left is None


@pytest.mark.django_db
def test_remove_some(product, user):
    quantity = 10
    to_consume = quantity // 2
    stock = product.transfer_in(user, quantity=quantity)

    stock_left = stock.remove(to_consume)
    assert stock.quantity == to_consume
    assert stock_left.quantity == quantity - to_consume
