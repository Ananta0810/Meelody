from abc import ABC, abstractmethod
from typing import List

from .class_name import ClassName


class PropsTranslator(ABC):
    @abstractmethod
    def id(self) -> str:
        pass

    @abstractmethod
    def translate(self, classNames: List[ClassName]) -> str:
        pass
