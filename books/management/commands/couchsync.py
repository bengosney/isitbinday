# Django
from django.core.management.base import BaseCommand, CommandError

# Locals
from ...models import SyncSetting
from ...services import sync_with_couchdb


class Command(BaseCommand):
    help = "Sync with CouchDB"

    def add_arguments(self, parser):
        parser.add_argument("id", type=int, help="ID to sync with CouchDB")

    def handle(self, *args, **options):
        id = options["id"]
        settings = SyncSetting.objects.get(pk=id)
        try:
            sync_with_couchdb(settings, lambda line: self.stdout.write(self.style.SUCCESS(line)))
            self.stdout.write(self.style.SUCCESS(f"Successfully synced with CouchDB for ID {id}"))
        except Exception as e:
            raise CommandError(f"Error syncing with CouchDB: {e}")
