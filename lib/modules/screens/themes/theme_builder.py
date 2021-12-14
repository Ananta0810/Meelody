from abc import ABC, abstractmethod


class ThemeData:
    def __init__(self, lightMode, darkMode):
        self.lightMode = lightMode
        self.darkMode = lightMode if darkMode is None else darkMode


class ThemeBuilder(ABC):
    @abstractmethod
    def build(self) -> ThemeData:
        pass
