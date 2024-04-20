from abc import ABC, abstractmethod
from typing import List

from PyQt5.QtWidgets import QWidget

from .class_name import ClassName


class PropsTranslator(ABC):
    @abstractmethod
    def id(self) -> str:
        pass

    @abstractmethod
    def translate(self, classNames: List[ClassName], target: QWidget) -> str:
        pass
