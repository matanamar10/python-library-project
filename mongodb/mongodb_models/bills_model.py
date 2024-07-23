from mongoengine import Document, StringField, FloatField


class Bill(Document):
    patron_id = StringField(required=True, unique=True, regex=r'^\d{9}$')
    amount = FloatField(required=True)
