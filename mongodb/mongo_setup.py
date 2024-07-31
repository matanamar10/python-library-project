from mongoengine import connect, disconnect


# Connect to MongoDB function
def connect_to_mongodb(settings):
    connect(db=settings.mongo_db_name, host=settings.mongo_client)


# Disconnect from MongoDB function
def disconnect_from_mongodb():
    disconnect()
