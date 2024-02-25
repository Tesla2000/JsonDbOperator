import json
import os
from pathlib import Path
from threading import Thread
from typing import Type, Any, Iterable, Sequence

from seriattrs import DbClass

from .abstract.DbClassOperator import DbClassOperator, T, NoSuchElementException


class JsonDbClassOperator(DbClassOperator):
    processing_file_prefix = 'processing_'

    def __init__(self, folder: Path, operated_class: Type[T]):
        self.folder = folder
        if not issubclass(operated_class, DbClass):
            raise ValueError("Operated class {} must be a subclass of DbClass".format(operated_class))
        self.operated_class = operated_class
        self.collection_name = operated_class.__name__
        self.collection_folder = self.folder.joinpath(self.collection_name)
        self.collection_folder.mkdir(parents=True, exist_ok=True)

    def delete(self, element: T) -> None:
        self.delete_by_id(str(element.id))

    def delete_by_id(self, element_id: Any) -> None:
        if not self.collection_folder.joinpath(str(element_id)).exists():
            raise NoSuchElementException("No element {} present in the database".format(element_id))
        os.remove(self.collection_folder.joinpath(str(element_id)))

    def load(self, object_id: Any) -> T:
        path = self.collection_folder.joinpath(str(object_id))
        if not path.exists():
            raise NoSuchElementException(
                "No element with id={} in the collection_name={}".format(object_id, self.collection_name)
            )
        return self.conv_to_seriattrs(path)

    def load_multiple(self, element_ids: Sequence[Any]) -> list[T]:
        results = [T for _ in element_ids]
        threads = tuple(
            Thread(target=lambda index, element_id: results.__setitem__(
                index, self.load(element_id)),
                   args=(index, element_id)) for index, element_id in enumerate(element_ids))
        tuple(map(Thread.start, threads))
        tuple(map(Thread.join, threads))
        return results

    def load_all(self) -> Iterable[T]:
        paths = self.collection_folder.iterdir()
        return map(self.conv_to_seriattrs, paths)

    def update(self, element: T) -> T:
        return self.write(element)

    def write(self, element: T) -> T:
        self.collection_folder.joinpath(self.processing_file_prefix + str(element.id)).write_text(
            json.dumps(element.serialize()))
        os.replace(self.collection_folder.joinpath(self.processing_file_prefix + str(element.id)),
                   self.collection_folder.joinpath(str(element.id)))
        return element

    def write_multiple(self, elements: Sequence[T]) -> list[T]:
        results = [T for _ in elements]
        threads = tuple(
            Thread(target=lambda index, element: results.__setitem__(
                index, self.write(element)),
                   args=(index, element)) for index, element in enumerate(elements))
        tuple(map(Thread.start, threads))
        tuple(map(Thread.join, threads))
        return results

    def conv_to_seriattrs(self, element_path: Path) -> T:
        dict_repr = json.loads(element_path.read_text())
        element = self.operated_class.deserialize(dict_repr)
        return element
