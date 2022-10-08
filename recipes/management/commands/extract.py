# Django
from django.core.management.base import BaseCommand

# First Party
from recipes.extrators import get_raw_html, schema_org


class Command(BaseCommand):
    help = "Test extracting"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("run"))

        url = "https://www.waitrose.com/ecom/recipe/vegan-banana-cake-with-chocolate-frosting"
        extractor = schema_org()

        rawHTML = get_raw_html(url)
        extractor.extract("".join(rawHTML))
