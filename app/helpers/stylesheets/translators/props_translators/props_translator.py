from abc import ABC, abstractmethod
from typing import List, TypeVar, Generic

T = TypeVar("T")


class PropsTranslator(Generic[T], ABC):
    @abstractmethod
    def id(self) -> str:
        pass

    @abstractmethod
    def translate(self, classNames: List[str]) -> T:
        pass
