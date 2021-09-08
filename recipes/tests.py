# Standard Library
import inspect
import random
import string
from abc import ABC

# Django
from django.contrib.auth.models import User
from django.urls import reverse

# Third Party
from rest_framework import status
from rest_framework.test import APITestCase

# Locals
from .models import Recipe


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
