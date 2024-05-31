# Standard Library
import datetime
import inspect

# Django
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

# Third Party
import pytest
from rest_framework import status

# Locals
from .models import Task
from .serializers import TaskSerializer


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


def test_requires_auth(client):
    url = reverse("tasks-api:task-list")
    response = client.get(url, format="json")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_create(authenticated_client):
    url = reverse("tasks-api:task-list")

    response = authenticated_client.post(url, {"title": "test task"}, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert Task.objects.count() == 1


@pytest.mark.django_db
def test_list(create_tasks, authenticated_client):
    url = reverse("tasks-api:task-list")
    create_tasks(5)

    response = authenticated_client.get(url, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert Task.objects.count() == int(response.json()["count"])


@pytest.mark.django_db
def test_list_only_mine(authenticated_client, create_tasks, insecure_password):
    url = reverse("tasks-api:task-list")
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


@pytest.mark.django_db
def test_task_serializer(task, snapshot):
    serializer = TaskSerializer(instance=task)

    data = serializer.data

    assert "created" in data.keys()
    del data["created"]

    assert "last_updated" in data.keys()
    del data["last_updated"]

    assert data == snapshot
