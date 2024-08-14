# Third Party
from couchdb import Server

# Locals
from ..models import Author, Book, SyncMetadata, SyncSetting


def sync_with_couchdb(setting: SyncSetting):
    server = Server(setting.connection_string())
    db = server[setting.database]

    for doc in db.view("_all_docs"):
        _id = doc.id
        _rev = doc.value["rev"]
        if meta := SyncMetadata.ensure(_id, _rev, setting):
            doc = db[_id]
            authors = []
            for author in doc["authors"]:
                author, _ = Author.objects.get_or_create(name=author, owner=setting.owner)
                authors.append(author)
            book, _ = Book.objects.update_or_create(
                isbn=doc["isbn"],
                defaults={
                    "title": doc["title"],
                    "cover": doc["cover"],
                    "requires_refetch": False,
                    "owner": setting.owner,
                },
            )
            book.authors.set(authors)
            book.save()
            meta.book = book
            meta._rev = _rev
            meta.save()
