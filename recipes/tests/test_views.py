# Standard Library
import inspect

# Django
from django.contrib.auth.models import User
from django.urls import reverse

# Third Party
import pytest
from rest_framework import status

# Locals
from ..models import Recipe


@pytest.mark.django_db
class TestRecipeViews:
    @pytest.fixture
    def create_recipes(self, api_client):
        def _create_recipes(count):
            url = reverse("recipe-list")
            for i in range(count):
                data = {
                    "name": f"{inspect.stack()[1].function} - {i}",
                    "time": f"0:{i}0:00",
                    "description": "string",
                    "link": "http://example.com",
                }
                response = api_client.post(url, data, format="json")
                assert response.status_code == status.HTTP_201_CREATED

        return _create_recipes

    def test_create(self, api_client):
        url = reverse("recipe-list")
        name = "Test Recipe"
        data = {
            "name": name,
            "time": "00:00:00",
            "description": "string",
            "link": "http://example.com",
        }

        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Recipe.objects.count() == 1
        assert Recipe.objects.get(name=name).name == name

    def test_list(self, api_client, create_recipes):
        url = reverse("recipe-list")
        count = 5

        create_recipes(count)

        response = api_client.get(url, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert Recipe.objects.count() == count
        assert Recipe.objects.count() == int(response.json()["count"])

    def test_list_only_mine(self, api_client, create_recipes, create_insecure_password):
        password = create_insecure_password()
        second_user = User.objects.create_user(username="keith", email="keith@example.com", password=password)

        url = reverse("recipe-list")
        count = 5

        create_recipes(count)
        api_client.logout()

        api_client.login(username=second_user.username, password=password)
        create_recipes(count)

        response = api_client.get(url, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert Recipe.objects.count() - count == int(response.json()["count"])
