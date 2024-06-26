# Standard Library
import datetime
import inspect
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


def get_insecure_password(length):
    return "".join(random.choice(string.ascii_lowercase) for _ in range(length))


class APITestCaseWithUser(ABC, APITestCase):
    def setUp(self):
        self.password = get_insecure_password(12)
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

    def create_tasks(self, count):
        url = reverse("task-list")
        for i in range(count):
            data = {
                "title": f"{inspect.stack()[1].function} - {i}",
            }
            self.client.post(url, data, format="json")

    def test_create(self, data={}):
        url = reverse("task-list")
        default_data = {
            "title": "test task",
        }

        response = self.client.post(url, {**default_data, **data}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)

    def test_list(self):
        url = reverse("task-list")
        count = 5

        self.create_tasks(count)

        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.count(), int(response.json()["count"]))

    def test_list_only_mine(self):
        password = get_insecure_password(12)
        second_user = User.objects.create_user(username="keith", email="keith@example.com", password=password)

        url = reverse("task-list")
        count = 5

        self.create_tasks(count)
        self.client.logout()

        self.client.login(username=second_user.username, password=password)
        self.create_tasks(count)

        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.count() - count, int(response.json()["count"]))


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

        tomorrow = timezone.make_aware(datetime.datetime.now() + datetime.timedelta(days=1))

        Task.auto_archive(tomorrow)
        archived_tasks = Task.objects.filter(state=Task.STATE_ARCHIVE)

        self.assertEqual(count, len(archived_tasks))
