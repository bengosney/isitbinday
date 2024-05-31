# Standard Library
import random
import string

# Django
from django.contrib.auth.models import User

# Third Party
import pytest


@pytest.fixture()
def insecure_password():
    return "".join(random.choice(string.ascii_lowercase) for _ in range(12))


@pytest.fixture
def user_password(insecure_password):
    user = User.objects.create_user(username="jacob", email="jacob@example.com", password=insecure_password)
    return user, insecure_password


@pytest.fixture
def user(user_password):
    return user_password[0]


@pytest.fixture
def authenticated_client(client, user_password):
    user, password = user_password
    client.login(username=user.username, password=password)
    return client
