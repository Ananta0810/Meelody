from abc import ABC, abstractmethod
from typing import List


class PropsTranslator(ABC):
    @abstractmethod
    def id(self) -> str:
        pass

    @abstractmethod
    def translate(self, classNames: List[str]) -> str:
        pass
