# Standard Library
import json

# Django
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.urls import reverse

# Third Party
from django_oso.models import AuthorizedModel
from requests import get


class Author(AuthorizedModel):

    # Relationships
    owner = models.ForeignKey("auth.User", related_name="authors", on_delete=models.CASCADE)

    # Fields
    name = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        unique_together = ["name", "owner"]

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("books_author_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("books_author_update", args=(self.pk,))


class Book(AuthorizedModel):

    # Relationships
    authors = models.ManyToManyField("books.Author", related_name="books")
    owner = models.ForeignKey("auth.User", related_name="books", on_delete=models.CASCADE)

    # Fields
    publish_date = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    title = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    isbn = models.CharField(max_length=30)

    class Meta:
        unique_together = [["isbn", "owner"], ["title", "owner"]]
        ordering = ["-pk"]

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("books_book_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("books_book_update", args=(self.pk,))

    @classmethod
    def get_or_lookup(cls, code: str, owner=None):
        try:
            return cls.objects.get(isbn=code)
        except ObjectDoesNotExist:
            return cls._lookup(code, owner=owner)

    @classmethod
    def _lookup(cls, code, owner=None):
        url = f"https://openlibrary.org/api/books?bibkeys={code}&jscmd=data&format=json"
        response = get(url)
        data = json.loads(response.text)[code]
        isbn = ""
        for ident in data["identifiers"]:
            if f"{ident}".startswith("isbn"):
                isbn = data["identifiers"][ident][0]

        book = Book(
            title=data["title"],
            isbn=isbn,
            publish_date=data["publish_date"],
            owner=owner,
        )

        book.save()

        for author_data in data["authors"]:
            author, _ = Author.objects.get_or_create(name=author_data["name"], owner=owner)
            book.authors.add(author)

        return book
