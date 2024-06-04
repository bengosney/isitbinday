# Standard Library

# Django
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

# Third Party
from faker import Faker

# Locals
from ...models import Task


class Command(BaseCommand):
    help = "Create some dummy data"

    def handle(self, *args, **options):
        self.stdout.write("Creating some dummy data")
        fake = Faker("en_GB")
        owner = User.objects.first()

        for state in Task.STATES:
            for _ in range(5 - Task.objects.filter(state=state).count()):
                task = Task.objects.create(title=fake.catch_phrase(), state=state, owner=owner)
                self.stdout.write(f"Created task {task}")
