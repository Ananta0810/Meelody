from abc import ABC, abstractmethod

from PyQt5.QtWidgets import QLabel, QLineEdit


class Text(ABC):
    @abstractmethod
    def exportLabel(self) -> QLabel:
        pass

    @abstractmethod
    def exportLineEdit(self) -> QLineEdit:
        pass
