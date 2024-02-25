from abc import ABC, abstractmethod
from typing import Any, Iterable, TypeVar, Sequence

from seriattrs import DbClass

T = TypeVar('T', bound=DbClass)


class DbClassOperator(ABC):
    @abstractmethod
    def delete(self, element: T) -> None:
        self.delete_by_id(str(element.id))

    @abstractmethod
    def delete_by_id(self, element_id: Any) -> None:
        pass

    @abstractmethod
    def load(self, object_id: Any) -> T:
        pass

    @abstractmethod
    def load_multiple(self, element_ids: Sequence[Any]) -> list[T]:
        pass

    @abstractmethod
    def load_all(self) -> Iterable[T]:
        pass

    @abstractmethod
    def update(self, element: T) -> T:
        pass

    @abstractmethod
    def write(self, element: T) -> T:
        pass

    @abstractmethod
    def write_multiple(self, elements: Sequence[T]) -> list[T]:
        pass

    @abstractmethod
    def conv_to_seriattrs(self, *args, **kwargs) -> T:
        pass


class NoSuchElementException(ValueError):
    pass
