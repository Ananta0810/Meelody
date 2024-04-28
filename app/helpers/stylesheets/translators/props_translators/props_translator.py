from abc import ABC, abstractmethod

from PyQt5.QtWidgets import QWidget

from .class_name import ClassName


class PropsTranslator(ABC):
    @abstractmethod
    def ids(self) -> set[str]:
        pass

    @abstractmethod
    def translate(self, classNames: list[ClassName], target: QWidget) -> str:
        pass
