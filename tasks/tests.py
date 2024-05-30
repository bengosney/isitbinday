# Standard Library
import datetime
import inspect
import random
import string

# Django
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

# Third Party
import pytest
from rest_framework import status

# Locals
from .models import Task


@pytest.fixture
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


@pytest.fixture
def create_tasks(authenticated_client):
    def _create_tasks(count, client=None):
        _client = client or authenticated_client
        url = reverse("tasks:task-list")
        for i in range(count):
            _client.post(url, {"title": f"{inspect.stack()[1].function} - {i}"}, format="json")

    return _create_tasks


def test_requires_auth(client):
    url = reverse("tasks:task-list")
    response = client.get(url, format="json")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_create(authenticated_client):
    url = reverse("tasks:task-list")

    response = authenticated_client.post(url, {"title": "test task"}, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert Task.objects.count() == 1


@pytest.mark.django_db
def test_list(create_tasks, authenticated_client):
    url = reverse("tasks:task-list")
    create_tasks(5)

    response = authenticated_client.get(url, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert Task.objects.count() == int(response.json()["count"])


@pytest.mark.django_db
def test_list_only_mine(authenticated_client, create_tasks, insecure_password):
    url = reverse("tasks:task-list")
    count = 5

    second_user = User.objects.create_user(username="keith", email="keith@example.com", password=insecure_password)
    for i in range(count):
        Task.objects.create(title=f"Other Task {i}", owner=second_user)

    create_tasks(count)

    response = authenticated_client.get(url, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert Task.objects.count() - count == int(response.json()["count"])


@pytest.mark.django_db
def test_str(user):
    title = "Test Task"
    task = Task(title=title, owner=user)

    assert title == f"{task.title}"


@pytest.mark.django_db
def test_completed_date(user):
    task = Task.objects.create(title="title", owner=user)
    task.done()

    assert task.completed is not None


@pytest.mark.django_db
def test_previous_state(user):
    task = Task.objects.create(title="title", owner=user)
    task.do()
    task.done()
    task.archive()
    task.save()

    assert task.previous_state == Task.STATE_DONE


@pytest.mark.django_db
def test_auto_archive(user):
    count = 5
    for i in range(count):
        task = Task.objects.create(title=f"Task {i}", owner=user)
        task.done()
        task.save()

    tomorrow = timezone.make_aware(datetime.datetime.now() + datetime.timedelta(days=1))

    Task.auto_archive(tomorrow)
    archived_tasks = Task.objects.filter(state=Task.STATE_ARCHIVE)

    assert count == len(archived_tasks)
