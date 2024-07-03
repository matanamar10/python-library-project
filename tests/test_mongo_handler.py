# test_mongo_handler.py
from mongodb.mongo_handler import (
    update_item_status, update_patron_items, insert_document, delete_document
)


def test_update_item_status(mock_db):
    update_item_status('123456789', True)
    item = mock_db['library-items'].find_one({'isbn': '123456789'})
    assert item['is_borrowed'] is True


def test_update_patron_items_borrow(mock_db):
    update_patron_items('111111111', '123456789', 'borrow')
    patron = mock_db['library-patrons'].find_one({'patron_id': '111111111'})
    assert '123456789' in patron['patron_items']


def test_update_patron_items_return(mock_db):
    update_patron_items('111111111', '123456789', 'return')
    patron = mock_db['library-patrons'].find_one({'patron_id': '111111111'})
    assert '123456789' not in patron['patron_items']


def test_insert_document(mock_db):
    new_doc = {'patron_id': '222222222', 'name': 'New Patron', 'patron_items': {}}
    inserted_id = insert_document('library-patrons', new_doc)
    inserted_doc = mock_db['library-patrons'].find_one({'_id': inserted_id})
    assert inserted_doc['patron_id'] == '222222222'


def test_delete_document(mock_db):
    result = delete_document('library-patrons', {'patron_id': '222222222'})
    assert result == 1
