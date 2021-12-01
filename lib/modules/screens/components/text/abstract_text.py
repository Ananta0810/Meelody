from abc import ABC, abstractmethod

from PyQt5.QtWidgets import QLineEdit


class AbstractLabel(ABC):
    @abstractmethod
    def render(self) -> QLineEdit:
        pass
