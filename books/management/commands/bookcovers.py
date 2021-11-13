# Django
from django.core.management.base import BaseCommand

# First Party
from books.models import Book


class Command(BaseCommand):
    help = "Fetch any book covers that need processing"

    def handle(self, *args, **options):
        books = Book.objects.filter(tmp_cover__isnull=False)

        for book in books:
            self.stdout.write(f"Processing {book.title}")
            if book.set_cover_from_tmp():
                book.save()

        self.stdout.write(self.style.SUCCESS(f"Processed {len(books)}"))
