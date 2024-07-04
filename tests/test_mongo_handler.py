# test_mongo_handler.py
from mongodb.mongo_handler import (
    update_item_status, update_patron_items, insert_document, delete_document
)


def test_update_patron_items_return(mock_db):
    update_patron_items('111111111', '123456789', 'return')
    patron = mock_db['library-patrons'].find_one({'patron_id': '111111111'})
    assert '123456789' not in patron['patron_items']
