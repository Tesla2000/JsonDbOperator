from pathlib import Path
from typing import Type

from seriattrs import DbClass

from .JsonDbClassOperator import JsonDbClassOperator
from .abstract.DbClassOperators import DbClassOperators


class JsonDbClassOperators(DbClassOperators):

    def __init__(self, folder: Path, dictionary: dict = None, **kwargs):
        self.folder = folder
        if dictionary is None:
            dictionary = {}
        super().__init__(dict(**dictionary, **kwargs))

    def _fill_missing(self, item: Type[DbClass]):
        return JsonDbClassOperator(self.folder, item)
