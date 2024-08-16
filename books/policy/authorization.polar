 
# Book Rules

allow(actor, "retrieve", book: books::Book) if
    book.owner = actor;

allow(actor, "retrieve", author: books::Author) if
    author.owner = actor;

allow(actor, "retrieve", author: books::SyncSetting) if
    author.owner = actor;
