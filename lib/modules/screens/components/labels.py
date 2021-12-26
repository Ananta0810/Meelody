from abc import ABC, abstractstaticmethod
from sys import path

# from modules.screens.qss.qss_elements import Padding
from PyQt5.QtCore import QObject, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLineEdit

path.append("./lib")
from modules.screens.components.view_item import ViewItem
from modules.screens.themes.theme_builder import ThemeBuilder
from modules.screens.themes.theme_builders import LabelThemeBuilder
from widgets.double_clicked_editable_label import QDoubleClickedEditableLabel
from widgets.label_with_default_text import LabelWithDefaultText
from widgets.placeholder_label import LabelWithPlaceholder


class ViewLabel(ViewItem, ABC):
    @abstractstaticmethod
    def render(
        font: QFont,
        parent: QObject,
    ):
        pass

    @abstractstaticmethod
    def getThemeBuilder() -> ThemeBuilder:
        return LabelThemeBuilder()


class StandardLabel(ViewLabel):
    def render(
        font: QFont,
        parent: QObject = None,
    ) -> QLineEdit:
        label = LabelWithDefaultText(parent)
        label.setFont(font)
        label.setReadOnly(True)
        label.setFocusPolicy(Qt.NoFocus)
        label.setStyleSheet("background:TRANSPARENT;border:none")
        return label

    def getThemeBuilder() -> ThemeBuilder:
        return LabelThemeBuilder()


class EditableLabel(ViewLabel):
    def render(
        font: QFont,
        parent: QObject = None,
    ) -> QLineEdit:
        label = LabelWithPlaceholder(parent)
        label.setFont(font)
        label.setStyleSheet("background:TRANSPARENT;border:none")
        return label

    def getThemeBuilder() -> ThemeBuilder:
        return LabelThemeBuilder()


class DoubleClickedEditableLabel(ViewLabel):
    def render(
        font: QFont,
        parent: QObject = None,
    ) -> QLineEdit:
        label = QDoubleClickedEditableLabel(parent)
        label.setFont(font)
        label.setStyleSheet("background:TRANSPARENT;border:none")
        return label

    def getThemeBuilder() -> ThemeBuilder:
        return LabelThemeBuilder()
