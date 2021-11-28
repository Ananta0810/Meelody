from abc import ABC, abstractmethod
from sys import path

from PyQt5.QtWidgets import QPushButton

path.append(".lib/modules/screens")

from modules.screens.background_color import BackgroundColor


class Button(ABC):
    def __init__(
        self,
        roundness: float,
        border: str,
        backgroundColor: BackgroundColor,
    ):
        self.roundness = roundness
        self.border = border
        self.backgroundColor = backgroundColor

    def withRoundness(self, roundness: float):
        self.roundness = roundness

    @abstractmethod
    def export(self) -> QPushButton:
        pass
