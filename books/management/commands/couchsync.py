# Django
from django.core.management.base import BaseCommand, CommandError

# Locals
from ...models import SyncSetting
from ...services import sync_with_couchdb


class Command(BaseCommand):
    help = "Sync with CouchDB"

    def add_arguments(self, parser):
        parser.add_argument("id", type=int, nargs="?", help="ID to sync with CouchDB")

    def handle(self, *args, **options):
        if id := options.get("id"):
            settings_to_process = [SyncSetting.objects.get(pk=id)]
        else:
            settings_to_process = SyncSetting.objects.all()

        for settings in settings_to_process:
            try:
                sync_with_couchdb(settings, lambda line: self.stdout.write(self.style.SUCCESS(line)))
                self.stdout.write(self.style.SUCCESS(f"Successfully synced with CouchDB for ID {id}"))
            except Exception as e:
                raise CommandError(f"Error syncing with CouchDB: {e}")
