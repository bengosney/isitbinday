# Django
from django.core.management.base import BaseCommand

# First Party
from books.models import Book


class Command(BaseCommand):
    help = "Refetch remote book data"

    def handle(self, *args, **options):
        books = Book.objects.filter(requires_refetch=True)

        for book in books:
            self.stdout.write(f"Refetching {book.title}")
            book.refetch_remote_data()

        self.stdout.write(self.style.SUCCESS(f"Refetched {len(books)}"))
