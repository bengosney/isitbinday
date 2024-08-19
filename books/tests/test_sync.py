# Standard Library
from unittest.mock import MagicMock, patch

# Django
from django.contrib.auth.models import User

# Third Party
import pytest
from couchdb import Database, Server

# Locals
from ..models import Author, Book, SyncSetting
from ..services.sync import get_author, process_doc, sync_with_couchdb


@pytest.fixture
def user(db):
    return User.objects.create(username="testuser")


@pytest.fixture
def author_name():
    return "John Doe"


@pytest.fixture
def book_doc(author_name):
    return {"isbn": "1234567890", "title": "Sample Book", "authors": [author_name], "cover": "sample_cover.jpg"}


@pytest.fixture
def sync_setting(user):
    return SyncSetting.objects.create(
        owner=user,
        database="test_db",
        username="test_user",
        password="test_password",
        server="couch.example.com",
    )


@pytest.fixture(autouse=True)
def clear_cache():
    get_author.cache_clear()


@pytest.fixture
def sample_doc():
    return {
        "id": "doc1",
        "key": "doc1",
        "value": {"rev": "1-abc"},
        "doc": {
            "type": "book",
            "isbn": "1234567890",
            "title": "Sample Book",
            "authors": ["John Doe"],
            "cover": "sample_cover.jpg",
        },
    }


@pytest.fixture
def mock_server(sample_doc):
    mock_doc = MagicMock()
    mock_doc.id.return_value = sample_doc["id"]
    mock_doc.value = sample_doc["value"]
    mock_db = MagicMock(spec=Database)
    mock_db.view.return_value = [mock_doc]
    mock_server = MagicMock(spec=Server)
    mock_server.__getitem__.return_value = mock_db
    return mock_server


def test_process_doc_new(user, book_doc):
    # Call the process_doc function for a new book
    returned_book = process_doc(book_doc, user)

    # Check if a new book is created
    assert isinstance(returned_book, Book)
    assert returned_book.title == book_doc["title"]
    assert returned_book.isbn == book_doc["isbn"]
    assert returned_book.tmp_cover == book_doc["cover"]
    assert not returned_book.requires_refetch
    assert returned_book.owner == user
    assert returned_book.authors.count() == 1
    author = returned_book.authors.first()
    assert isinstance(author, Author)
    assert author.name == book_doc["authors"][0]


def test_process_doc_existing(user, book_doc):
    # Create an existing book
    existing_book = Book.objects.create(
        isbn=book_doc["isbn"], title="Old Title", tmp_cover="old_cover.jpg", requires_refetch=True, owner=user
    )
    existing_author = Author.objects.create(name=book_doc["authors"][0], owner=user)
    existing_book.authors.add(existing_author)

    # Call the process_doc function to update the existing book
    returned_book = process_doc(book_doc, user)

    # Check if the existing book is updated
    assert returned_book == existing_book
    assert returned_book.title == book_doc["title"]
    assert returned_book.tmp_cover == book_doc["cover"]
    assert not returned_book.requires_refetch
    assert returned_book.owner == user
    assert returned_book.authors.count() == 1
    author = returned_book.authors.first()
    assert isinstance(author, Author)
    assert author.name == book_doc["authors"][0]


def test_get_author_existing(user, author_name):
    # Create an existing author
    author = Author.objects.create(name=author_name, owner=user)

    # Call the get_author function
    returned_author = get_author(author_name, user)

    # Check if the returned author is the same as the existing author
    assert returned_author == author


def test_get_author_new(user, author_name):
    # Call the get_author function for a new author
    returned_author = get_author(author_name, user)

    # Check if a new author is created
    assert isinstance(returned_author, Author)


def test_sync_with_couchdb(sync_setting, sample_doc, mock_server):
    wrapped_process_doc = MagicMock(wraps=process_doc)

    with (
        patch("books.services.sync.Server", return_value=mock_server),
        patch("books.services.sync.process_doc", wrapped_process_doc),
        patch("books.services.sync.fetch_doc", return_value=sample_doc["doc"]),
    ):
        sync_with_couchdb(sync_setting)
        wrapped_process_doc.assert_called_once_with(sample_doc["doc"], sync_setting.owner)

    books = Book.objects.all()
    assert books.count() == 1
    book = books.first()
    assert book is not None
    assert book.isbn == sample_doc["doc"]["isbn"]
