from abc import ABC, abstractmethod
from sys import path

from PyQt5.QtWidgets import QPushButton

path.append(".lib/modules/screens")


class Button(ABC):
    @abstractmethod
    def render(self) -> QPushButton:
        pass
