from typing import Type

try:
    from pymongo.database import Database
except ModuleNotFoundError:
    raise ModuleNotFoundError("Pymongo not found. Install pymongo before using MongoDbOperator")
from seriattrs import DbClass

from .MongoDbClassOperator import MongoDbClassOperator
from .abstract.DbClassOperators import DbClassOperators


class MongoDbClassOperators(DbClassOperators):

    def __init__(self, db: Database, dictionary: dict = None, **kwargs):
        self.db = db
        if dictionary is None:
            dictionary = {}
        super().__init__(dict(**dictionary, **kwargs))

    def _fill_missing(self, item: Type[DbClass]):
        return MongoDbClassOperator(self.db, item)
