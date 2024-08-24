# Django
from django.contrib.auth.models import User

# Third Party
import pytest

# Locals
from ..models import Author, Book, FailedScan, SyncMetadata, SyncSetting


@pytest.fixture
def user():
    return User.objects.create(username="testuser")


@pytest.fixture
def author(user):
    return Author.objects.create(name="John Doe", owner=user)


@pytest.fixture
def another_user():
    return User.objects.create(username="Jane Doe")


@pytest.fixture
def failed_scan(user):
    return FailedScan.objects.create(isbn="1234567890", owner=user)


@pytest.fixture
def book(user, author):
    book = Book.objects.create(title="Test Book", isbn="1234567890123", owner=user)
    book.authors.add(author)
    return book


@pytest.fixture
def sync_setting(user):
    return SyncSetting.objects.create(
        owner=user,
        database="test_db",
        username="test_user",
        password="test_password",
        server="couch.example.com",
    )


@pytest.fixture
def sync_metadata(user, sync_setting, book):
    return SyncMetadata.objects.create(owner=user, server=sync_setting, book=book, _id="test_id", _rev="test_rev")
