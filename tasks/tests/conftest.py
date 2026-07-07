# Standard Library
import datetime
import random
import string

# Django
from django.contrib.auth.models import User
from django.utils import timezone

# Third Party
import pytest
from model_bakery import baker
from rest_framework.test import APIClient

# Locals
from ..models import Task


@pytest.fixture
def create_insecure_password():
    return lambda: "".join(random.choice(string.ascii_lowercase) for _ in range(12))


@pytest.fixture
def insecure_password(create_insecure_password):
    return create_insecure_password()


@pytest.fixture
def user(db, insecure_password):
    return User.objects.create_user(username="jacob", password=insecure_password)


@pytest.fixture
def api_client(user, insecure_password):
    client = APIClient()
    client.login(username=user.username, password=insecure_password)
    return client


@pytest.fixture
def create_tasks(create_task):
    def _create_tasks(count):
        for _ in range(count):
            create_task()

    return _create_tasks


@pytest.fixture
def create_task(user):
    def _create_task():
        return baker.make(Task, owner=user)

    return _create_task


@pytest.fixture
def create_done_task(create_task):
    def _create_done_task():
        with create_task() as task:
            task.done()
            task.save()
            return task

    return _create_done_task


@pytest.fixture
def tomorrow():
    return timezone.make_aware(datetime.datetime.now() + datetime.timedelta(days=1))
