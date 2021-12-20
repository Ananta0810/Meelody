from abc import ABC, abstractmethod

from modules.screens.themes.theme_builders import ThemeData


class Ui(ABC):
    @abstractmethod
    def lightMode(self):
        pass

    @abstractmethod
    def darkMode(self):
        pass

    @abstractmethod
    def __addThemeForItem(self, item, theme: ThemeData) -> None:
        pass

    @abstractmethod
    def __addButtonToList(self, button) -> None:
        pass
