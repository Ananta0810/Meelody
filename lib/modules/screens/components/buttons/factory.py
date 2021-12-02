from abc import ABC, abstractmethod

from PyQt5.QtWidgets import QPushButton


class ButtonFactory(ABC):
    @abstractmethod
    def getButtonByType(self) -> QPushButton:
        pass
