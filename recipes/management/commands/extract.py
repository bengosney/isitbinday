# Django
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

# Locals
from ...extractors import SchemaOrg


class Command(BaseCommand):
    help = "Test extracting"

    def add_arguments(self, parser):
        parser.add_argument("owner", type=int)
        parser.add_argument("url", type=str)

    def handle(self, *args, **options):
        if "url" not in options:
            raise Exception("URL not specified")

        url = options["url"]
        self.stdout.write(self.style.SUCCESS(f"Getting recipe from {url}"))

        owner = User.objects.get(pk=options["owner"])

        if owner is None:
            raise Exception(f"User with id {options['owner']} was not found")

        extractor = SchemaOrg(owner)
        extractor.extract(url)
