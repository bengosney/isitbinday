# Standard Library
import json

# Django
from django.urls import reverse
from django.utils.http import urlencode

# Third Party
from rest_framework import status

# First Party
from food.models import Stock

# Locals
from .base import APIBaseTestCase


class testProductAPI(APIBaseTestCase):
    def setUp(self):
        super().setUp()
        self.login()

    def test_transfer_in(self):
        url = reverse("product-transfer-in", kwargs={"code": self.product.code})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        stocks = self.product.stocks.all()
        self.assertEqual(len(stocks), 1)
        self.assertEqual(stocks[0].quantity, 1)
        self.assertEqual(stocks[0].state, Stock.STATE_IN_STOCK)

    def test_transfer_quantity_in(self, quantity=10):
        url = reverse("product-transfer-in", kwargs={"code": self.product.code})
        urlWithQuery = f"{url}?{urlencode({'quantity': quantity})}"
        response = self.client.get(urlWithQuery, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        stocks = self.product.stocks.all()
        self.assertEqual(len(stocks), 1)
        self.assertEqual(stocks[0].quantity, quantity)
        self.assertEqual(stocks[0].state, Stock.STATE_IN_STOCK)

    def test_transfer_pack_in(self, quantity=2):
        url = reverse("product-transfer-in", kwargs={"code": self.pack.code})
        urlWithQuery = f"{url}?{urlencode({'quantity': quantity})}"
        response = self.client.get(urlWithQuery, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        stocks = self.pack.stocks.all()
        self.assertEqual(len(stocks), 1)
        self.assertEqual(stocks[0].quantity, quantity * self.pack.quantity)
        self.assertEqual(stocks[0].state, Stock.STATE_IN_STOCK)

    def test_consume_some(self, quantity=10):
        stock = self.product.transfer_in(self.user, quantity)
        url = reverse("stock-consume", kwargs={"pk": stock.pk})
        toConsume = quantity // 2
        urlWithQuery = f"{url}?{urlencode({'quantity': toConsume})}"
        response = self.client.get(urlWithQuery, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        content = json.loads(response.content)
        self.assertEqual(content["quantity"], quantity - toConsume)
