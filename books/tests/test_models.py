# Standard Library
import json

# Django
from django.db.utils import IntegrityError

# Third Party
import pytest

# Locals
from ..models import Author, Book, FailedScan, NotFoundError, SyncMetadata, SyncSetting


@pytest.mark.django_db
def test_author_unique_constraint(user, another_user):
    Author.objects.create(name="Unique Author", owner=user)
    Author.objects.create(name="Unique Author", owner=another_user)

    with pytest.raises(IntegrityError):
        Author.objects.create(name="Unique Author", owner=user)


@pytest.mark.django_db
def test_author_creation(user):
    author = Author.objects.create(name="Jane Doe", owner=user)
    assert author.name == "Jane Doe"
    assert author.owner == user


@pytest.mark.django_db
def test_author_str(author):
    assert str(author) == "John Doe"


@pytest.mark.django_db
def test_failed_scan_creation(user):
    failed_scan = FailedScan.objects.create(isbn="0987654321", owner=user)
    assert failed_scan.isbn == "0987654321"
    assert failed_scan.owner == user


@pytest.mark.django_db
def test_failed_scan_unique_constraint(user, another_user):
    FailedScan.objects.create(isbn="1234567890", owner=user)
    FailedScan.objects.create(isbn="1234567890", owner=another_user)

    with pytest.raises(IntegrityError):
        FailedScan.objects.create(isbn="1234567890", owner=user)


@pytest.mark.django_db
def test_failed_scan_str(failed_scan):
    assert str(failed_scan) == "1234567890"


@pytest.mark.django_db
def test_sync_setting_unique_constraint(user, another_user):
    SyncSetting.objects.create(
        owner=user, server="test_server", database="test_database", username="test_user", password="test_password"
    )
    SyncSetting.objects.create(
        owner=another_user,
        server="test_server",
        database="test_database",
        username="test_user",
        password="test_password",
    )
    with pytest.raises(IntegrityError):
        SyncSetting.objects.create(
            owner=user,
            server="test_server",
            database="test_database",
            username="another_user",
            password="another_password",
        )


@pytest.mark.django_db
def test_sync_setting_str(sync_setting):
    assert str(sync_setting) == f"{sync_setting.server}/{sync_setting.database}"


@pytest.mark.django_db
def test_sync_setting_connection_string(sync_setting):
    expected_connection_string = f"https://{sync_setting.username}:{sync_setting.password}@{sync_setting.server}"
    assert sync_setting.connection_string() == expected_connection_string


@pytest.mark.django_db
def test_sync_metadata_creation(user, sync_setting, book):
    sync_metadata = SyncMetadata.objects.create(
        owner=user, server=sync_setting, book=book, _id="test_id", _rev="test_rev"
    )
    assert sync_metadata.owner == user
    assert sync_metadata.server == sync_setting
    assert sync_metadata.book == book
    assert sync_metadata._id == "test_id"
    assert sync_metadata._rev == "test_rev"


@pytest.mark.django_db
def test_sync_metadata_str(sync_metadata):
    assert str(sync_metadata) == "test_id - test_rev"


@pytest.mark.django_db
def test_sync_metadata_ensure(user, sync_setting):
    sync_metadata = SyncMetadata.ensure(id="test_id", rev="new_rev", server=sync_setting)
    assert sync_metadata is not None
    assert sync_metadata._id == "test_id"
    assert sync_metadata._rev == "new_rev"
    assert sync_metadata.server == sync_setting
    assert sync_metadata.owner == sync_setting.owner


@pytest.mark.django_db
def test_book_unique_constraints(user, another_user):
    Book.objects.create(title="Unique Book", isbn="1234567890", owner=user)
    Book.objects.create(title="Unique Book", isbn="1234567890", owner=another_user)

    with pytest.raises(IntegrityError):
        Book.objects.create(title="Unique Book", isbn="1234567890", owner=user)


@pytest.mark.django_db
def test_book_str(book):
    assert str(book) == book.title


@pytest.mark.django_db
def test_book_lookup_google(mocker, user):
    mock_response = mocker.Mock()
    mock_response.text = json.dumps(
        {
            "items": [
                {
                    "volumeInfo": {
                        "title": "Google Book",
                        "publishedDate": "2020",
                        "imageLinks": {"thumbnail": "http://example.com/cover.jpg"},
                        "authors": ["Author 1"],
                    }
                }
            ]
        }
    )
    mocker.patch("requests.get", return_value=mock_response)

    book = Book._lookup_google("1234567890", owner=user)
    assert book.title == "Google Book"
    assert book.publish_date == "2020"
    assert book.tmp_cover == "http://example.com/cover.jpg"
    assert book.authors.count() == 1


@pytest.mark.django_db
def test_book_lookup_open_books(mocker, user):
    mock_response = mocker.Mock()
    mock_response.text = json.dumps(
        {
            "ISBN:1234567890": {
                "title": "Open Book",
                "publish_date": "2021",
                "covers": {"large": "http://example.com/cover.jpg"},
                "authors": [{"name": "Author 2"}],
                "identifiers": {"isbn_10": ["1234567890"]},
            }
        }
    )
    mocker.patch("requests.get", return_value=mock_response)

    book = Book._lookup_open_books("ISBN:1234567890", owner=user)
    assert book.title == "Open Book"
    assert book.publish_date == "2021"
    assert book.tmp_cover == "http://example.com/cover.jpg"
    assert book.authors.count() == 1


@pytest.mark.django_db
def test_book_lookup_fallback(mocker, user):
    mocker.patch("books.models.Book._lookup_google", side_effect=NotFoundError)
    mocker.patch(
        "books.models.Book._lookup_open_books", return_value=Book(title="Fallback Book", isbn="1234567890", owner=user)
    )

    book = Book._lookup("1234567890", owner=user)
    assert book.title == "Fallback Book"


@pytest.mark.django_db
def test_book_refetch_remote_data(mocker, book):
    mocker.patch("books.models.Book._lookup", return_value=book)

    book.refetch_remote_data()
    assert book.requires_refetch is False


@pytest.mark.django_db
def test_book_get_or_lookup_get(user, book):
    looked_up_book = Book.get_or_lookup(book.isbn, owner=user)
    assert looked_up_book.title == book.title


@pytest.mark.django_db
def test_book_get_or_lookup_lookup(mocker, user):
    mocker.patch("books.models.Book._lookup", return_value=Book(title="Lookup Book", isbn="1234567890", owner=user))

    book = Book.get_or_lookup("1234567890", owner=user)
    assert book.title == "Lookup Book"
