# Standard Library
import datetime
import random
import string
from abc import ABC

# Django
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

# Third Party
from rest_framework import status
from rest_framework.test import APITestCase

# Locals
from .models import Task


def getInsecurePassword(length):
    return "".join(random.choice(string.ascii_lowercase) for i in range(length))  # nosec


class APITestCaseWithUser(ABC, APITestCase):
    def setUp(self):
        self.password = getInsecurePassword(12)
        self.user = User.objects.create_user(username="jacob", email="jacob@example.com", password=self.password)


class TaskAuthTestCase(APITestCaseWithUser):
    def test_requires_auth(self):
        url = reverse("task-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TaskViewsTestCase(APITestCaseWithUser):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.user.username, password=self.password)

    def test_create(self):
        url = reverse("task-list")
        data = {
            "title": "test task",
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TaskModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="jacob", email="jacob@example.com")

    def test_str(self):
        title = "Test Task"
        task = Task(title=title, owner=self.user)

        self.assertEqual(title, f"{task.title}")

    def test_completed_date(self):
        task = Task.objects.create(title="title", owner=self.user)
        task.done()

        self.assertIsNotNone(task.completed)

    def test_previous_state(self):
        task = Task.objects.create(title="title", owner=self.user)
        task.do()
        task.done()
        task.archive()
        task.save()

        self.assertEqual(task.previous_state, Task.STATE_DONE)

    def test_auto_archive(self):
        count = 5
        for i in range(count):
            task = Task.objects.create(title=f"Task {i}", owner=self.user)
            task.done()
            task.save()

        tomorrow = timezone.make_aware(datetime.datetime.today() + datetime.timedelta(days=1))
        Task.auto_archive(tomorrow)
        archivedTasks = Task.objects.filter(state=Task.STATE_ARCHIVE)

        self.assertEqual(count, len(archivedTasks))
