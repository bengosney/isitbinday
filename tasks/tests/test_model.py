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
    create_tasks(5)

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


@pytest.mark.django_db
def test_str(user):
    title = "Test Task"
    task = Task(title=title, owner=user)

    assert title == f"{task.title}"


@pytest.mark.django_db
def test_completed_date(create_task):
    with create_task() as task:
        task.done()

    assert task.completed is not None


@pytest.mark.django_db
def test_previous_state(create_task):
    with create_task() as task:
        task.do()
        task.done()

    assert task.previous_state == Task.STATE_DOING


@pytest.mark.django_db
def test_auto_archive(create_done_task, create_task, tomorrow):
    create_done_task()
    create_done_task()
    create_done_task()
    create_task()

    Task.auto_archive(tomorrow)
    archived_tasks = Task.objects.filter(archived=Task.ARCHIVE_STATE_ARCHIVED)

    assert len(archived_tasks) == 3


@pytest.mark.django_db
def test_auto_archive_not_done(create_task, tomorrow):
    task = create_task()
    Task.auto_archive(tomorrow)
    refreshed_task = Task.objects.get(pk=task.pk)
    assert refreshed_task.state == Task.STATE_TODO


@pytest.mark.django_db
def test_auto_archive_no_tasks(tomorrow):
    Task.auto_archive(tomorrow)
    assert Task.objects.count() == 0
