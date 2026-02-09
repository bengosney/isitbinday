# Standard Library
import random
import string
from abc import ABC

# Django
from django.contrib.auth.models import User

# Third Party
from rest_framework.test import APITestCase


def get_insecure_password(length):
    return "".join(random.choice(string.ascii_lowercase) for _ in range(length))


class APITestCaseWithUser(ABC, APITestCase):
    def setUp(self):
        self.password = get_insecure_password(12)
        self.user = User.objects.create_user(username="jacob", email="jacob@example.com", password=self.password)
