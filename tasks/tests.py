# Standard Library
import datetime

# Django
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

# Locals
from .models import Task


class TaskTestCase(TestCase):
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
