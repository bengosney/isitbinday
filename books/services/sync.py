# Standard Library
from collections.abc import Callable
from functools import lru_cache

# Django
from django.contrib.auth.models import User
from django.db import transaction

# Third Party
from couchdb import Server

# Locals
from ..models import Author, Book, SyncMetadata, SyncSetting


@lru_cache
def get_author(name: str, owner: User) -> Author:
    return Author.objects.get_or_create(name=name, owner=owner)[0]


def sync_with_couchdb(setting: SyncSetting, logger: Callable[[str], None] = lambda _: None):
    server = Server(setting.connection_string())
    db = server[setting.database]

    for doc in db.view("_all_docs"):
        _id = doc.id
        _rev = doc.value["rev"]
        if meta := SyncMetadata.ensure(_id, _rev, setting):
            doc = db[_id]
            if doc["type"] != "book":
                continue

            logger(f"Processing {doc['title']}")

            with transaction.atomic():
                authors = [get_author(author, owner=setting.owner) for author in doc["authors"]]
                book, _ = Book.objects.update_or_create(
                    isbn=doc["isbn"],
                    defaults={
                        "title": doc["title"],
                        "tmp_cover": doc.get("cover", ""),
                        "requires_refetch": "cover" not in doc,
                        "owner": setting.owner,
                    },
                )
                book.authors.set(authors)
                book.save()
                meta.book = book
                meta._rev = _rev
                meta.save()
