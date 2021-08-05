# Django
from django.test import TestCase

# Locals
from .models import Book


class BookModelTestCase(TestCase):
    def test_lookup(self):
        self.assertEqual(True, False)
        return
        isbn = "9781985232822"
        book = Book._lookup(isbn)

        self.assertEqual(book.isbn, isbn)
