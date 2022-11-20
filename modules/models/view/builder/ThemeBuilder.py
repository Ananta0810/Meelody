from abc import abstractmethod, ABC

from modules.models.view.Background import Background


class ThemeData:
    def __init__(self, light_mode, dark_mode=None):
        self.light_mode = light_mode
        self.dark_mode = dark_mode or light_mode

    def __str__(self):
        return f"Light mode: {self.light_mode}, Dark mode: {self.dark_mode}"


class ThemeBuilder(ABC):
    @abstractmethod
    def addLightModeBackground(self, background: Background):
        pass

    @abstractmethod
    def addDarkModeBackground(self, background: Background):
        pass

    @abstractmethod
    def build(self, size: int) -> ThemeData:
        pass
