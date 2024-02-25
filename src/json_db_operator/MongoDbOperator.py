try:
    from pymongo.database import Database
except ModuleNotFoundError:
    raise ModuleNotFoundError("Pymongo not found. Install pymongo before using MongoDbOperator")

from .MongoDbClassOperators import MongoDbClassOperators
from .abstract.DbOperator import DbOperator


class MongoDbOperator(DbOperator):

    def __init__(self, db: Database):
        self.db = db
        self._known_classes = MongoDbClassOperators(db)

    def clear_database(self):
        collection_names = self.db.list_collection_names()

        for collection_name in collection_names:
            collection = self.db[collection_name]
            collection.delete_many({})
