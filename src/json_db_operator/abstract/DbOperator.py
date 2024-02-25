from abc import abstractmethod
from typing import Type, Iterable, Any, Sequence

from .DbClassOperator import T, NoSuchElementException
from .DbClassOperators import DbClassOperators


class DbOperator:
    _known_classes: DbClassOperators

    def delete(self, element: T) -> None:
        self._known_classes[type(element)].delete(element)

    def delete_by_id(self, element_class: Type[T], element_id: Any) -> None:
        self._known_classes[element_class].delete_by_id(element_id)

    def load(self, element_class: Type[T], element_id: Any) -> T:
        return self._known_classes[element_class].load(element_id)

    def load_multiple(self, element_class: Type[T], element_ids: Sequence[Any]) -> list[T]:
        return self._known_classes[element_class].load_multiple(element_ids)

    def load_or_default(self, element_class: Type[T], element_id: Any, default=None) -> T:
        try:
            return self.load(element_class, element_id)
        except NoSuchElementException:
            return default

    def conv_to_seriattrs(self, element_class: Type[T], doc) -> T:
        return self._known_classes[element_class].conv_to_seriattrs(doc)

    def load_all(self, element_class: Type[T]) -> Iterable[T]:
        return self._known_classes[element_class].load_all()

    def update(self, element: T) -> T:
        return self._known_classes[type(element)].update(element)

    def write(self, element: T) -> T:
        return self._known_classes[type(element)].write(element)

    def write_multiple(self, elements: Sequence[T]) -> list[T]:
        if elements:
            return self._known_classes[type(elements[0])].write_multiple(elements)
        return []

    @abstractmethod
    def clear_database(self):
        pass
