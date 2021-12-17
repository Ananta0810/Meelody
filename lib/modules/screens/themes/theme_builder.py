from abc import ABC, abstractmethod


class ThemeData:
    def __init__(self, lightMode, darkMode):
        self.lightMode = lightMode
        self.darkMode = darkMode or lightMode

    def __str__(self):
        return f"Light: {self.lightMode}, Dark: {self.darkMode}"


class ThemeBuilder(ABC):
    @abstractmethod
    def build(self) -> ThemeData:
        pass
