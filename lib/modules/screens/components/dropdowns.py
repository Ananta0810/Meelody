from sys import path

path.append("./lib")
from modules.screens.components.view_item import ViewItem
from modules.screens.themes.theme_builder import ThemeBuilder
from modules.screens.themes.theme_builders import DropdownMenuThemeBuilder
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QComboBox, QStyledItemDelegate


class DropdownMenu(ViewItem):
    def render(self):
        dropdownMenu = QComboBox()
        dropdownMenu.setItemDelegate(QStyledItemDelegate())
        dropdownMenu.view().window().setWindowFlags(
            Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint
        )
        dropdownMenu.view().window().setAttribute(Qt.WA_TranslucentBackground)
        return dropdownMenu

    def getThemeBuilder(self) -> ThemeBuilder:
        return DropdownMenuThemeBuilder()
