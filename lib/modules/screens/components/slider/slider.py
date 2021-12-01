from abc import ABC, abstractmethod

from PyQt5.QtWidgets import QSlider


class Slider(ABC):
    @abstractmethod
    def render(self) -> QSlider:
        pass
