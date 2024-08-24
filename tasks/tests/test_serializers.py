# Standard Library
from datetime import datetime

# Third Party
import pytest

# Locals
from ..models import Task
from ..serializers import TaskSerializer


@pytest.fixture
def task(user):
    return Task.objects.create(
        title="Sample Task",
        due_date=datetime.now().date(),
        effort=5,
        owner=user,
        state="open",
        position=1,
    )


@pytest.fixture
def task_data(user):
    return {
        "title": "Sample Task",
        "due_date": "2023-10-10",
        "effort": 5,
        "owner": user.username,
        "state": "doing",
        "position": 1,
    }


@pytest.mark.django_db
def test_task_serializer_serialization(task):
    serializer = TaskSerializer(task)
    data = serializer.data
    assert data["title"] == task.title
    assert data["effort"] == task.effort
    assert data["owner"] == task.owner.username
    assert data["state"] == task.state
    assert data["position"] == task.position


@pytest.mark.django_db
def test_task_serializer_deserialization(task_data, user):
    serializer = TaskSerializer(data=task_data)
    assert serializer.is_valid(), serializer.errors
    task = serializer.save(owner=user)
    assert task.title == task_data["title"]
    assert task.effort == task_data["effort"]
    assert task.owner == user
    assert task.state != task_data["state"]
    assert task.position == task_data["position"]


@pytest.mark.django_db
def test_task_serializer_read_only_fields(task):
    serializer = TaskSerializer(task)
    data = serializer.data
    assert "owner" in data
    assert "completed" in data
    assert "state" in data
    assert serializer.fields["owner"].read_only
    assert serializer.fields["completed"].read_only
    assert serializer.fields["state"].read_only


@pytest.mark.django_db
def test_task_serializer_to_internal_value(task_data):
    task_data["due_date"] = ""
    serializer = TaskSerializer(data=task_data)
    assert serializer.is_valid(), serializer.errors
    validated_data = serializer.validated_data
    assert "due_date" not in validated_data
