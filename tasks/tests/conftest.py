# Standard Library
import inspect
import random
import string

# Django
from django.contrib.auth.models import User
from django.urls import reverse

# Third Party
import pytest
from rest_framework.test import APIClient


@pytest.fixture
def create_insecure_password():
    return lambda: "".join(random.choice(string.ascii_lowercase) for _ in range(12))


@pytest.fixture
def insecure_password(create_insecure_password):
    return create_insecure_password()


@pytest.fixture
@pytest.mark.django_db
def user(insecure_password):
    return User.objects.create_user(username="jacob", password=insecure_password)


@pytest.fixture
@pytest.mark.django_db
def api_client(user, insecure_password):
    client = APIClient()
    client.login(username=user.username, password=insecure_password)
    return client


@pytest.fixture
@pytest.mark.django_db
def create_tasks(api_client):
    def _create_tasks(count):
        url = reverse("task-list")
        for i in range(count):
            data = {"title": f"{inspect.stack()[1].function} - {i}"}
            api_client.post(url, data, format="json")

    return _create_tasks
