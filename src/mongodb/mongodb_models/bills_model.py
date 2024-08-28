from mongoengine import Document, StringField, FloatField

from src.env_utils import MongoDBSettings


class BillDocument(Document):
    patron_id = StringField(required=True, unique=True, regex=r'^\d{9}$')
    patron_bill_sum = FloatField(required=True)
    meta = {
        'collection': MongoDBSettings().mongo_bills_collection
    }
