# Standard Library
from collections.abc import Callable
from functools import lru_cache
from typing import Any

# Django
from django.contrib.auth.models import User
from django.db import transaction

# Third Party
from couchdb import Database, Server
from couchdb.http import ResourceNotFound
from ratelimit import limits, sleep_and_retry

# Locals
from ..models import Author, Book, SyncMetadata, SyncSetting


@lru_cache
def get_author(name: str, owner: User) -> Author:
    return Author.objects.get_or_create(name=name, owner=owner)[0]


def process_doc(doc: dict[str, Any], owner: User) -> Book:
    authors = [get_author(author, owner=owner) for author in doc["authors"]]
    book, _ = Book.objects.update_or_create(
        isbn=doc["isbn"],
        defaults={
            "title": doc["title"],
            "tmp_cover": doc.get("cover", ""),
            "requires_refetch": "cover" not in doc,
            "owner": owner,
        },
    )
    book.authors.set(authors)
    book.save()

    return book


@sleep_and_retry
@limits(calls=1, period=1)
def fetch_doc(doc_id: str, db: Database) -> dict[str, Any] | None:
    try:
        return db[doc_id]
    except ResourceNotFound:
        return None


def sync_with_couchdb(setting: SyncSetting, logger: Callable[[str], None] = lambda _: None) -> None:
    server = Server(setting.connection_string())
    db = server[setting.database]

    for doc in db.view("_all_docs"):
        _id = doc.id
        _rev = doc.value["rev"]
        if meta := SyncMetadata.ensure(_id, _rev, setting):
            doc = fetch_doc(_id, db)
            if doc is None or doc["type"] != "book":
                continue

            logger(f"Processing {doc['title']}")

            with transaction.atomic():
                book = process_doc(doc, setting.owner)
                meta.book = book
                meta._rev = _rev
                meta.save()
