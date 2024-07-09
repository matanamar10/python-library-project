from mongoengine import Document, StringField, FloatField
from mongodb.mongo_setup import settings


class Bill(Document):
    patron_id = StringField(required=True, unique=True, regex=r'^\d{9}$')
    amount = FloatField(required=True)
    meta = {'collection': settings.mongo_bills_collection}
