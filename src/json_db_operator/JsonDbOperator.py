import os
from pathlib import Path
from typing import Type, Iterable, Any, Sequence, TypeVar

from seriattrs import DbClass

from .JsonDbClassOperator import NoSuchElementException
from .JsonDbClassOperators import JsonDbClassOperators
from .abstract.DbOperator import DbOperator

T = TypeVar('T', bound=DbClass)


class JsonDbOperator(DbOperator):
    def __init__(self, folder: Path):
        self.folder = folder
        self.folder.mkdir(parents=True, exist_ok=True)
        self._known_classes = JsonDbClassOperators(folder)

    def clear_database(self):
        for dirpath, dirnames, filenames in os.walk(self.folder):
            for file in filenames:
                os.remove(os.path.join(dirpath, file))
