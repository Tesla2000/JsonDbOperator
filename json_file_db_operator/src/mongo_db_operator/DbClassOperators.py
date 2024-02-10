from pathlib import Path
from typing import Type

from seriattrs import DbClass

from .DbClassOperator import DbClassOperator


class DbClassOperators(dict):
    def __init__(self, folder: Path, dictionary: dict = None, **kwargs):
        self.folder = folder
        if dictionary is None:
            dictionary = {}
        super().__init__(dict(**dictionary, **kwargs))

    def __getitem__(self, item: Type[DbClass]) -> DbClassOperator:
        if not issubclass(item, DbClass):
            raise ValueError("Item must be a subclass of DbClass")
        try:
            return super().__getitem__(item)
        except KeyError:
            self[item] = DbClassOperator(self.folder, item)
            return self[item]
