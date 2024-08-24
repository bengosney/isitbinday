# Standard Library

# Django
from django.contrib.auth.models import User
from django.urls import reverse

# Third Party
import pytest
from rest_framework import status
from rest_framework.test import APIClient

# Locals
from ..models import Task


@pytest.mark.django_db
def test_requires_auth():
    url = reverse("task-list")
    api_client = APIClient()
    response = api_client.get(url, format="json")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_create_task(api_client):
    url = reverse("task-list")
    default_data = {
        "title": "test task",
    }

    response = api_client.post(url, default_data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert Task.objects.count() == 1


@pytest.mark.django_db
def test_list(api_client, create_tasks):
    url = reverse("task-list")
    count = 5
    create_tasks(count)

    response = api_client.get(url, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert Task.objects.count() == int(response.json()["count"])


@pytest.mark.django_db
def test_list_only_mine(create_tasks, create_insecure_password):
    second_client = APIClient()
    password = create_insecure_password()
    second_user = User.objects.create_user(username="keith", password=password)
    second_client.login(username=second_user.username, password=password)

    create_tasks(5)

    url = reverse("task-list")
    response = second_client.get(url, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert int(response.json()["count"]) == 0
