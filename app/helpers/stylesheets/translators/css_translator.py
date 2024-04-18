from abc import ABC, abstractmethod
from typing import List, TypeVar, Generic

T = TypeVar("T")


class CssTranslator(Generic[T], ABC):
    @abstractmethod
    def translate(self, classNames: List[str]) -> T:
        pass
