# Standard Library
import json

# Django
from django.urls import reverse
from django.utils.http import urlencode

# Third Party
import pytest
from rest_framework import status

# Locals
from ..models import Stock


@pytest.mark.django_db
def test_transfer_in(authenticated_client, product):
    url = reverse("food:product-transfer-in", kwargs={"code": product.code})
    response = authenticated_client.get(url, format="json")
    assert response.status_code == status.HTTP_200_OK

    stocks = product.stocks.all()
    assert len(stocks) == 1
    assert stocks[0].quantity == 1
    assert stocks[0].state == Stock.STATE_IN_STOCK


@pytest.mark.django_db
def test_transfer_quantity_in(authenticated_client, product):
    quantity = 10
    url = reverse("food:product-transfer-in", kwargs={"code": product.code})
    url_with_query = f"{url}?{urlencode({'quantity': quantity})}"
    response = authenticated_client.get(url_with_query, format="json")
    assert response.status_code == status.HTTP_200_OK

    stocks = product.stocks.all()
    assert len(stocks) == 1
    assert stocks[0].quantity == quantity
    assert stocks[0].state == Stock.STATE_IN_STOCK


@pytest.mark.django_db
def test_transfer_pack_in(authenticated_client, pack):
    quantity = 2
    url = reverse("food:product-transfer-in", kwargs={"code": pack.code})
    url_with_query = f"{url}?{urlencode({'quantity': quantity})}"
    response = authenticated_client.get(url_with_query, format="json")
    assert response.status_code == status.HTTP_200_OK

    stocks = pack.stocks.all()
    assert len(stocks) == 1
    assert stocks[0].quantity == quantity * pack.quantity
    assert stocks[0].state == Stock.STATE_IN_STOCK


@pytest.mark.django_db
def test_consume_some(authenticated_client, product, user):
    quantity = 10
    stock = product.transfer_in(user, quantity)
    url = reverse("food:stock-consume", kwargs={"pk": stock.pk})
    to_consume = quantity // 2
    url_with_query = f"{url}?{urlencode({'quantity': to_consume})}"
    response = authenticated_client.get(url_with_query, format="json")

    assert response.status_code == status.HTTP_200_OK
    content = json.loads(response.content)
    assert content["quantity"] == quantity - to_consume
