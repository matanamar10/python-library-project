from models.library_items.items import LibraryItem  # Your existing Pydantic model
from models.patrons.patron import Patron
from mongodb.mongodb_models.library_item_model import LibraryItemDocument
from mongodb.mongodb_models.patron_model import PatronDocument


def item_pydantic_to_mongoengine(item: LibraryItem) -> LibraryItemDocument:
    return LibraryItemDocument(
        is_borrowed=item.is_borrowed,
        title=item.title,
        isbn=item.isbn
    )


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
