# Django
from django.core.management.base import BaseCommand

# First Party
from recipes.extrators import schema_org


class Command(BaseCommand):
    help = "Test extracting"

    def add_arguments(self, parser):
        parser.add_argument("url", type=str)

    def handle(self, *args, **options):
        if "url" not in options:
            raise Exception("URL not specified")

        url = options["url"]
        self.stdout.write(self.style.SUCCESS(f"Getting recipe from {url}"))

        extractor = schema_org()
        extractor.extract(url)
