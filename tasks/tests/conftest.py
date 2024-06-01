# Standard Library
import inspect

# Django
from django.urls import reverse

# Third Party
import pytest

# Locals
from ..models import Task


@pytest.fixture
def create_tasks(authenticated_client):
    def _create_tasks(count, client=None):
        _client = client or authenticated_client
        url = reverse("tasks-api:task-list")
        for i in range(count):
            _client.post(url, {"title": f"{inspect.stack()[1].function} - {i}"}, format="json")

    return _create_tasks


@pytest.fixture
def task(user):
    return Task.objects.create(title="Test Task", owner=user)
