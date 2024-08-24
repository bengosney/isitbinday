# Third Party
import pytest
from couchdb import Database, Server

# Locals
from ..models import Author, Book
from ..services.sync import get_author, process_doc, sync_with_couchdb


@pytest.fixture
def author_name():
    return "John Doe"


@pytest.fixture
def book_doc(author_name):
    return {"isbn": "1234567890", "title": "Sample Book", "authors": [author_name], "cover": "sample_cover.jpg"}


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
def mock_server(mocker, sample_doc):
    mock_doc = mocker.MagicMock(id=sample_doc["id"], value=sample_doc["value"])
    mock_db = mocker.MagicMock(spec=Database)
    mock_db.view.return_value = [mock_doc]
    mock_server = mocker.MagicMock(spec=Server)
    mock_server.__getitem__.return_value = mock_db

    return mock_server


@pytest.mark.django_db
def test_process_doc_new(user, book_doc, check):
    # Call the process_doc function for a new book
    returned_book = process_doc(book_doc, user)

    # Check if a new book is created
    assert isinstance(returned_book, Book)
    check.equal(returned_book.title, book_doc["title"])
    check.equal(returned_book.isbn, book_doc["isbn"])
    check.equal(returned_book.tmp_cover, book_doc["cover"])
    check.is_false(returned_book.requires_refetch)
    check.equal(returned_book.owner, user)
    check.equal(returned_book.authors.count(), 1)

    author = returned_book.authors.first()
    assert isinstance(author, Author)
    check.equal(author.name, book_doc["authors"][0])


@pytest.mark.django_db
def test_process_doc_existing(user, book_doc, check):
    # Create an existing book
    existing_book = Book.objects.create(
        isbn=book_doc["isbn"], title="Old Title", tmp_cover="old_cover.jpg", requires_refetch=True, owner=user
    )
    existing_author = Author.objects.create(name=book_doc["authors"][0], owner=user)
    existing_book.authors.add(existing_author)

    # Call the process_doc function to update the existing book
    returned_book = process_doc(book_doc, user)

    # Check if the existing book is updated
    check.equal(returned_book, existing_book)
    check.equal(returned_book.title, book_doc["title"])
    check.equal(returned_book.tmp_cover, book_doc["cover"])
    check.is_false(returned_book.requires_refetch)
    check.equal(returned_book.owner, user)
    check.equal(returned_book.authors.count(), 1)

    author = returned_book.authors.first()
    assert isinstance(author, Author)
    check.equal(author.name, book_doc["authors"][0])


@pytest.mark.django_db
def test_get_author_existing(user, author_name):
    # Create an existing author
    author = Author.objects.create(name=author_name, owner=user)

    # Call the get_author function
    returned_author = get_author(author_name, user)

    # Check if the returned author is the same as the existing author
    assert returned_author == author


@pytest.mark.django_db
def test_get_author_new(user, author_name):
    # Call the get_author function for a new author
    returned_author = get_author(author_name, user)

    # Check if a new author is created
    assert isinstance(returned_author, Author)


@pytest.mark.django_db
def test_sync_with_couchdb(sync_setting, sample_doc, mock_server, check, mocker):
    wrapped_process_doc = mocker.MagicMock(wraps=process_doc)

    mocker.patch("books.services.sync.Server", return_value=mock_server)
    mocker.patch("books.services.sync.process_doc", wrapped_process_doc)
    mocker.patch("books.services.sync.fetch_doc", return_value=sample_doc["doc"])

    sync_with_couchdb(sync_setting)
    wrapped_process_doc.assert_called_once_with(sample_doc["doc"], sync_setting.owner)

    books = Book.objects.all()
    check.equal(books.count(), 1)
    book = books.first()
    assert book is not None
    check.equal(book.isbn, sample_doc["doc"]["isbn"])
