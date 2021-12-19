from abc import ABC, abstractmethod
from sys import path

path.append(".\lib")
from sys import path

from modules.screens.themes.theme_builder import ThemeBuilder


class ViewItem(ABC):
    @abstractmethod
    def render(self):
        pass

    @abstractmethod
    def getThemeBuilder(self) -> ThemeBuilder:
        pass
