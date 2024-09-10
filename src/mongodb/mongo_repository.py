# mongodb/mongo_repository.py

from typing import List, Optional
from src.mongodb.mongodb_models.library_item_model import LibraryItemDocument
from typing import Dict
from src.mongodb.mongodb_models.patron_model import PatronDocument
from src.mongodb.mongodb_models.bills_model import BillDocument


class MongoLibraryItemRepository:
    async def update_item_status(self, isbn: str, is_borrowed: bool) -> None:
        item = await LibraryItemDocument.find_one(LibraryItemDocument.isbn == isbn)
        if item:
            item.is_borrowed = is_borrowed
            await item.save()

    async def insert_document(self, document: LibraryItemDocument) -> None:
        await document.insert()

    async def delete_document(self, query: Dict[str, str]) -> None:
        await LibraryItemDocument.find(query).delete()

    async def item_exists(self, isbn: str) -> bool:
        return await LibraryItemDocument.find(LibraryItemDocument.isbn == isbn).count() > 0

    async def is_item_borrowed(self, isbn: str) -> bool:
        item = await LibraryItemDocument.find_one(LibraryItemDocument.isbn == isbn)
        return item.is_borrowed if item else False

    async def search_items(self, query: Dict[str, Optional[str]]) -> List[LibraryItemDocument]:
        return await LibraryItemDocument.find(query).to_list()


class MongoPatronRepository:
    async def return_item(self, patron_id: str, isbn: str) -> None:
        patron = await PatronDocument.find_one(PatronDocument.id == patron_id)
        if patron:
            patron.items.pop(isbn, None)
            await patron.save()

    async def borrow_item(self, patron_id: str, isbn: str, borrow_date) -> None:
        patron = await PatronDocument.find_one(PatronDocument.id == patron_id)
        if patron:
            patron.items[isbn] = borrow_date
            await patron.save()

    async def insert_document(self, document: PatronDocument) -> None:
        await document.insert()

    async def delete_document(self, query: Dict) -> None:
        await PatronDocument.find(query).delete()

    async def patron_exists(self, patron_id: str) -> bool:
        return await PatronDocument.find(PatronDocument.id == patron_id).count() > 0


class MongoBillRepository:
    async def insert_bill(self, patron_id: str, amount: float) -> None:
        bill = BillDocument(patron_id=patron_id, patron_bill_sum=amount)
        await bill.insert()

    async def update_bill(self, patron_id: str, amount: float) -> None:
        bill = await BillDocument.find_one(BillDocument.patron_id == patron_id)
        if bill:
            bill.patron_bill_sum = amount
            await bill.save()

    async def delete_bill(self, patron_id: str) -> None:
        await BillDocument.find(BillDocument.patron_id == patron_id).delete()
