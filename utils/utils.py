from models.entities.library_items import Book
from models.entities.library_items.disks.disks import Disk
from models.entities.library_items import LibraryItem  # Your existing Pydantic model
from models.entities.patrons import Patron
from mongodb.mongodb_models.book_model import BookDocument
from mongodb.mongodb_models.disk_model import DiskDocument
from mongodb.mongodb_models.library_item_model import LibraryItemDocument
from mongodb.mongodb_models.patron_model import PatronDocument


def item_pydantic_to_mongoengine(item: LibraryItem) -> LibraryItemDocument:
    if isinstance(item, Book):
        return BookDocument(
            is_borrowed=item.is_borrowed,
            title=item.title,
            isbn=item.isbn,
            type="Book",
            author=item.author
        )
    elif isinstance(item, Disk):
        return DiskDocument(
            is_borrowed=item.is_borrowed,
            title=item.title,
            isbn=item.isbn,
            type="Disk",
            disk_type=item.disk_type
        )
    else:
        raise ValueError(f"Unsupported library item type: {type(item).__name__}")


def item_mongoengine_to_pydantic(item_document: LibraryItemDocument) -> LibraryItem:
    return LibraryItem(
        is_borrowed=item_document.is_borrowed,
        title=item_document.title,
        isbn=item_document.isbn
    )


def patron_pydantic_to_mongoengine(patron: Patron) -> PatronDocument:
    return PatronDocument(
        name=patron.name,
        patron_id=patron.patron_id,
        patron_items=patron.patron_items
    )


def patron_mongoengine_to_pydantic(patron_document: PatronDocument) -> Patron:
    return Patron(
        name=patron_document.name,
        patron_id=patron_document.patron_id,
        patron_items=patron_document.patron_items
    )
