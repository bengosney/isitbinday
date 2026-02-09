# Standard Library
import random
import string

# Django
from django.contrib.auth.models import User

# Third Party
import pytest
from rest_framework.test import APIClient

# Locals
from ..models import Unit


@pytest.fixture
def create_insecure_password():
    return lambda length=12: "".join(random.choice(string.ascii_lowercase) for _ in range(length))


@pytest.fixture
def insecure_password(create_insecure_password):
    return create_insecure_password()


@pytest.fixture
def user(db, insecure_password):
    return User.objects.create_user(username="jacob", email="jacob@example.com", password=insecure_password)


@pytest.fixture
def api_client(user, insecure_password):
    client = APIClient()
    client.login(username=user.username, password=insecure_password)
    return client


@pytest.fixture
def unit_of(db):
    unit, _ = Unit.objects.get_or_create(name="of")
    return unit
