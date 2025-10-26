# Standard Library
from unittest import mock

# Django
from django.contrib.auth import get_user_model
from django.urls import reverse

# Third Party
import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_google_login_missing_token():
    url = reverse("accounts:google-login")
    client = APIClient()
    response = client.post(url, {})
    assert response.status_code == 400
    assert "token" in response.data


@pytest.mark.django_db
def test_google_login_invalid_token():
    url = reverse("accounts:google-login")
    client = APIClient()
    with mock.patch("accounts.views.id_token.verify_oauth2_token", side_effect=Exception("bad token")):
        response = client.post(url, {"token": "invalid"})
    assert response.status_code == 400
    assert "error" in response.data


@pytest.mark.django_db
def test_google_login_valid_token_creates_user(settings):
    url = reverse("accounts:google-login")
    client = APIClient()
    user_model = get_user_model()
    fake_idinfo = {
        "email": "testuser@gmail.com",
        "given_name": "Test",
        "family_name": "User",
    }
    settings.GOOGLE_OAUTH_CLIENT_ID = "fake-client-id"
    with mock.patch("accounts.views.id_token.verify_oauth2_token", return_value=fake_idinfo):
        with mock.patch("accounts.views.google_requests.Request"):
            response = client.post(url, {"token": "valid"})
    assert response.status_code == 200
    data = response.json()
    assert "access" in data
    assert "refresh" in data
    assert user_model.objects.filter(email="testuser@gmail.com").exists()


@pytest.mark.django_db
def test_google_login_existing_user(settings):
    url = reverse("accounts:google-login")
    client = APIClient()
    user_model = get_user_model()
    user_model.objects.create_user(
        email="testuser@gmail.com",
        username="testuser@gmail.com",
        first_name="Test",
        last_name="User",
        password="pass",
        is_active=True,
    )
    fake_idinfo = {
        "email": "testuser@gmail.com",
        "given_name": "Test",
        "family_name": "User",
    }
    settings.GOOGLE_OAUTH_CLIENT_ID = "fake-client-id"
    with mock.patch("accounts.views.id_token.verify_oauth2_token", return_value=fake_idinfo):
        with mock.patch("accounts.views.google_requests.Request"):
            response = client.post(url, {"token": "valid"})
    assert response.status_code == 200
    data = response.json()
    assert "access" in data
    assert "refresh" in data


@pytest.mark.django_db
def test_google_login_existing_user_alias(settings):
    url = reverse("accounts:google-login")
    client = APIClient()
    user_model = get_user_model()
    user_model.objects.create_user(
        email="testuser@googlemail.com",
        username="testuser@googlemail.com",
        first_name="Test",
        last_name="User",
        password="pass",
        is_active=True,
    )
    fake_idinfo = {
        "email": "testuser@gmail.com",
        "given_name": "Test",
        "family_name": "User",
    }
    settings.GOOGLE_OAUTH_CLIENT_ID = "fake-client-id"
    with mock.patch("accounts.views.id_token.verify_oauth2_token", return_value=fake_idinfo):
        with mock.patch("accounts.views.google_requests.Request"):
            response = client.post(url, {"token": "valid"})
    assert response.status_code == 200
    data = response.json()
    assert "access" in data
    assert "refresh" in data
