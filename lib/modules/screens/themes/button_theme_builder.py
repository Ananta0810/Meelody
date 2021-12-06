from abc import ABC, abstractmethod

from modules.screens.qss.qss_elements import QSSBackground, Color

from .theme_builder import ThemeBuilder, ThemeHolder


class ButtonThemeBuilder(ThemeBuilder, ABC):
    @abstractmethod
    def addColor(self, color: QSSBackground):
        pass

    @abstractmethod
    def addLightModeBackground(self, background: QSSBackground):
        pass

    @abstractmethod
    def addDarkModeBackground(self, background: QSSBackground):
        pass

    @abstractmethod
    def addLightModeActiveBackground(self, background: QSSBackground):
        pass

    @abstractmethod
    def addDarkModeActiveBackground(self, background: QSSBackground):
        pass

    @abstractmethod
    def build(self) -> ThemeHolder:
        pass


class StandardIconButtonThemeBuilder(ButtonThemeBuilder):
    def __init__(self):
        self.lightModeBackground = None
        self.darkModeBackground = None
        self.lightModeCheckedBackground = None
        self.darkModeCheckedBackground = None

    def addColor(self, color: Color):
        return self

    def addLightModeBackground(self, background: QSSBackground):
        self.lightModeBackground = background
        return self

    def addDarkModeBackground(self, background: QSSBackground):
        self.darkModeBackground = background
        return self

    def addLightModeActiveBackground(self, background: QSSBackground):
        return self

    def addDarkModeActiveBackground(self, background: QSSBackground):
        return self

    def build(self, itemSize) -> ThemeHolder:
        lightMode = self.__buildTheme(itemSize, self.lightModeBackground)
        darkMode = self.__buildTheme(itemSize, self.darkModeBackground)
        return ThemeHolder(lightMode, darkMode)

    def __buildTheme(self, itemSize, background: QSSBackground) -> str:
        if background is None:
            return None
        return BackgroundStyleSheet().export(
            "QPushButton", itemSize, color=None, background=background
        )


class BackgroundStyleSheet:
    def export(
        self,
        element: str,
        elementSize: float,
        color: Color,
        background: QSSBackground,
    ):
        return (
            f"{element}"
            + "{"
            + f"  color:None;"
            + f"  border:{background.borderStyleSheet()};"
            + f"  border-radius:{background.borderRadiusStyleSheet(elementSize)};"
            + f"  background-color:{background.colorStyleSheet()};"
            + "}"
            + f"{element}:hover"
            + "{"
            + f"  border:{background.borderStyleSheet(active=True)};"
            + f"  background-color:{background.colorStyleSheet(active=True)};"
            + "}"
        )


class ToggleIconButtonThemeBuilder(ButtonThemeBuilder):
    def __init__(self):
        self.lightModeBackground = None
        self.darkModeBackground = None
        self.lightModeCheckedBackground = None
        self.darkModeCheckedBackground = None

    def addColor(self, color: Color):
        return self

    def addLightModeBackground(self, background: QSSBackground):
        self.lightModeBackground = background
        return self

    def addDarkModeBackground(self, background: QSSBackground):
        self.darkModeBackground = background
        return self

    def addLightModeActiveBackground(self, background: QSSBackground):
        self.lightModeCheckedBackground = background
        return self

    def addDarkModeActiveBackground(self, background: QSSBackground):
        self.darkModeCheckedBackground = background
        return self

    def build(self, itemSize: int) -> ThemeHolder:
        lightMode = (
            None
            if self.lightModeBackground is None
            and self.lightModeCheckedBackground is None
            else self.__buildTheme(
                itemSize,
                self.lightModeBackground,
                self.lightModeCheckedBackground,
            )
        )
        darkMode = (
            lightMode
            if self.darkModeBackground is None
            and self.darkModeCheckedBackground is None
            else self.__buildTheme(
                itemSize,
                self.darkModeBackground,
                self.darkModeCheckedBackground,
            )
        )
        return ThemeHolder(lightMode, darkMode)

    def __buildTheme(
        self,
        buttonSize,
        background: QSSBackground,
        checkedBackground: QSSBackground,
    ):
        styleSheet = ""
        if background is not None:
            styleSheet += BackgroundStyleSheet().export(
                "QPushButton", buttonSize, None, background
            )
        if checkedBackground is not None:
            styleSheet += BackgroundStyleSheet().export(
                "QPushButton:checked", buttonSize, None, checkedBackground
            )
        return styleSheet
