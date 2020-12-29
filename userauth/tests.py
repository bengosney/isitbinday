# Standard Library
import random
import string

# Django
from django.contrib.auth.models import User
from django.urls import reverse

# Third Party
from rest_framework import status
from rest_framework.test import APITestCase


def getInsecurePassword(length: int):
    return "".join(random.choice(string.ascii_lowercase) for i in range(length))  # nosec


class TaskModelTestCase(APITestCase):
    def setUp(self):
        self.password: str = getInsecurePassword(12)
        self.user: User = User.objects.create_user(username="jacob", email="jacob@example.com", password=self.password)
        self.url = reverse("task-list")

    def test_nothing(self):
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_username(self):
        self.client.login(username=self.user.username, password=self.password)
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_email(self):
        self.client.login(username=self.user.email, password=self.password)
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
