from abc import abstractmethod
from pathlib import Path
from typing import Type

from seriattrs import DbClass

from .DbClassOperator import DbClassOperator


class DbClassOperators(dict):
    @abstractmethod
    def _fill_missing(self, item: Type[DbClass]):
        pass

    def __getitem__(self, item: Type[DbClass]) -> DbClassOperator:
        if not issubclass(item, DbClass):
            raise ValueError("Item must be a subclass of DbClass")
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            self[item] = self._fill_missing(item)
            return self[item]
