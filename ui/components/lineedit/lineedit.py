from abc import ABC, abstractmethod

from PyQt5.QtWidgets import QLineEdit


class LineEdit(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def produce(self) -> QLineEdit:
        pass
