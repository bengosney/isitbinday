# Django
from django.core.management.base import BaseCommand

# First Party
from books.models import Book


class Command(BaseCommand):
    help = "Fetch any book covers that need processing"

    def add_arguments(self, parser):
        parser.add_argument("limit", type=int)

    def handle(self, *args, **options):
        limit = options["limit"]
        books = Book.objects.filter(tmp_cover__isnull=False)[:limit]

        for book in books:
            self.stdout.write(f"Processing {book.title}")
            if book.set_cover_from_tmp():
                book.save()

        self.stdout.write(self.style.SUCCESS(f"Processed {len(books)}"))
