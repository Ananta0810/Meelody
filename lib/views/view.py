from typing import Optional

from modules.screens.themes.theme_builders import ThemeData
from PyQt5.QtWidgets import QPushButton, QWidget


class View:
    def __init__(self) -> None:
        self.itemsWithTheme: dict[Optional["QWidget"], ThemeData] = {}
        self.buttonsWithDarkMode: list[QPushButton] = []

    def connectController(self, controller) -> None:
        pass

    def lightMode(self) -> None:
        for button in self.buttonsWithDarkMode:
            button.setDarkMode(False)
        for item in self.itemsWithTheme:
            lightModeStyleSheet = self.itemsWithTheme.get(item).lightMode
            if lightModeStyleSheet is None or lightModeStyleSheet.strip() == "":
                continue
            item.setStyleSheet(lightModeStyleSheet)

    def darkMode(self) -> None:
        for button in self.buttonsWithDarkMode:
            button.setDarkMode(True)
        for item in self.itemsWithTheme:
            darkModeStyleSheet = self.itemsWithTheme.get(item).darkMode
            if darkModeStyleSheet is None or darkModeStyleSheet.strip() == "":
                continue
            item.setStyleSheet(darkModeStyleSheet)

    def _addThemeForItem(self, item: QWidget, theme: ThemeData) -> None:
        self.itemsWithTheme[item] = theme

    def _addButtonToList(self, item: QPushButton) -> None:
        self.buttonsWithDarkMode.append(item)
