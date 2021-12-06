from abc import ABC, abstractmethod


class ThemeHolder:
    def __init__(self, lightMode, darkMode):
        self.lightMode = lightMode
        self.darkMode = lightMode if darkMode is None else darkMode


class ThemeBuilder(ABC):
    @abstractmethod
    def build(self) -> ThemeHolder:
        pass
