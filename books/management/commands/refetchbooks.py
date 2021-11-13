# Django
from django.core.management.base import BaseCommand

# First Party
from books.models import Book


class Command(BaseCommand):
    help = "Refetch remote book data"

    def add_arguments(self, parser):
        parser.add_argument("limit", type=int)

    def handle(self, *args, **options):
        limit = options["limit"]
        books = Book.objects.filter(requires_refetch=True)[:limit]

        for book in books:
            self.stdout.write(f"Refetching {book.title}")
            book.refetch_remote_data()

        self.stdout.write(self.style.SUCCESS(f"Refetched {len(books)}"))
