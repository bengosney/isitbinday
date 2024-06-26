# Standard Library
import json
import mimetypes

# Django
from django.core import files
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.temp import NamedTemporaryFile
from django.db import models, transaction
from django.urls import reverse
from django.utils.text import slugify

# Third Party
import requests
from django_oso.models import AuthorizedModel
from requests import get


class NotFoundError(Exception):
    pass


class Author(AuthorizedModel):
    class Meta:
        unique_together = ["name", "owner"]

    # Relationships
    owner = models.ForeignKey("auth.User", related_name="authors", on_delete=models.CASCADE)

    # Fields
    name = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    def get_absolute_url(self):
        return reverse("books_author_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("books_author_update", args=(self.pk,))

    def __str__(self):
        return str(self.name)


class FailedScan(AuthorizedModel):
    class Meta:
        unique_together = ["isbn", "owner"]

    owner = models.ForeignKey("auth.User", related_name="failedBookScan", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    isbn = models.CharField(max_length=30)

    def __str__(self) -> str:
        return f"{self.isbn}"


class Book(AuthorizedModel):
    class Meta:
        unique_together = [["isbn", "owner"], ["title", "owner"]]
        ordering = ["-pk"]

    # Relationships
    authors = models.ManyToManyField("books.Author", related_name="books")
    owner = models.ForeignKey("auth.User", related_name="books", on_delete=models.CASCADE)

    # Fields
    publish_date = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    title = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    isbn = models.CharField(max_length=30)

    cover = models.ImageField(upload_to="book/cover", blank=True, default="")
    tmp_cover = models.CharField(max_length=512, blank=True, default="")

    requires_refetch = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("books_book_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("books_book_update", args=(self.pk,))

    def set_cover_from_tmp(self):
        if self.tmp_cover is None:
            return False

        try:
            request = requests.get(self.tmp_cover, stream=True)
        except requests.exceptions.RequestException:
            self.tmp_cover = None
            return True

        if request.status_code != requests.codes.ok:
            self.tmp_cover = None
            return True

        try:
            content_type = request.headers["content-type"]
            ext = mimetypes.guess_extension(content_type)
        except AttributeError:
            ext = ""

        f = NamedTemporaryFile(delete=True)

        for block in request.iter_content(1024 * 8):
            if not block:
                break

            f.write(block)

        f.flush()
        self.cover = files.File(f, name=f"{slugify(self.title)}-cover{ext}")
        self.tmp_cover = None
        return True

    @classmethod
    @transaction.atomic
    def _lookup_google(cls, code, owner=None):
        url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{code}"
        response = get(url)

        try:
            data = json.loads(response.text)["items"][0]["volumeInfo"]
        except AttributeError as e:
            raise NotFoundError from e

        defaults = {
            "title": data["title"],
            "publish_date": data["publishedDate"],
            "requires_refetch": False,
        }

        try:
            defaults["tmp_cover"] = data["imageLinks"]["thumbnail"]
        except AttributeError:
            pass

        book, _ = Book.objects.update_or_create(isbn=code, owner=owner, defaults=defaults)

        for author_data in data["authors"]:
            author, _ = Author.objects.get_or_create(name=author_data, owner=owner)
            book.authors.add(author)

        return book

    @classmethod
    @transaction.atomic
    def _lookup_open_books(cls, code, owner=None):
        url = f"https://openlibrary.org/api/books?bibkeys={code}&jscmd=data&format=json"
        response = get(url)

        try:
            data = json.loads(response.text)[code]
        except AttributeError as e:
            raise NotFoundError from e

        isbn = ""
        for ident in data["identifiers"]:
            if f"{ident}".startswith("isbn"):
                isbn = data["identifiers"][ident][0]

        defaults = {
            "title": data["title"],
            "publish_date": data["publish_date"],
            "requires_refetch": False,
        }

        try:
            defaults["tmp_cover"] = data["covers"]["large"]
        except AttributeError:
            pass

        book, _ = Book.objects.update_or_create(
            isbn=isbn,
            owner=owner,
            defaults=defaults,
        )

        for author_data in data["authors"]:
            author, _ = Author.objects.get_or_create(name=author_data["name"], owner=owner)
            book.authors.add(author)

        return book

    @classmethod
    def _lookup(cls, code, owner=None, create_fail=True):
        try:
            return cls._lookup_google(code, owner)
        except Exception:
            pass

        try:
            return cls._lookup_open_books(code, owner)
        except Exception:
            pass

        if create_fail:
            try:
                fail = FailedScan(isbn=code, owner=owner)
                fail.save()
            except Exception:
                pass

        raise Exception("Failed to lookup")

    def refetch_remote_data(self):
        try:
            self._lookup(self.isbn, owner=self.owner)
        except Exception:
            pass

    @classmethod
    def get_or_lookup(cls, code: str, owner=None):
        try:
            return cls.objects.get(isbn=code)
        except ObjectDoesNotExist:
            return cls._lookup(code, owner=owner)

    def __str__(self):
        return f"{self.title}"
