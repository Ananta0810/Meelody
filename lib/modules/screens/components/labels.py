from abc import ABC, abstractmethod
from sys import path

from modules.screens.qss.qss_elements import Padding
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLineEdit

path.append("./lib")
from modules.screens.components.view_item import ViewItem
from modules.screens.themes.theme_builder import ThemeBuilder
from modules.screens.themes.theme_builders import LabelThemeBuilder
from widgets.label_with_default_text import LabelWithDefaultText
from widgets.placeholder_label import LabelWithPlaceholder


class ViewLabel(ViewItem):
    @abstractmethod
    def render(
        self,
        font: QFont,
        padding: Padding,
        alignment,
        parent,
    ):
        pass


class StandardLabel(ViewLabel):
    def render(
        self,
        font: QFont,
        padding: Padding = None,
        alignment=None,
        parent=None,
    ) -> QLineEdit:
        label = LabelWithDefaultText(parent)
        label.setFont(font)
        label.setReadOnly(True)
        if alignment is not None:
            label.setAlignment(alignment)
        width = label.sizeHint().width()
        height = label.sizeHint().height()
        if padding is not None:
            width += padding.getWidth(width)
            height += padding.getHeight(height)
        label.setBaseSize(width, height)
        label.setStyleSheet("background:transparent;border:none")
        return label

    def getThemeBuilder(self) -> ThemeBuilder:
        return LabelThemeBuilder()


class EditableLabel(ViewLabel):
    def render(
        self,
        font: QFont,
        padding: Padding = None,
        alignment=None,
        parent=None,
    ) -> QLineEdit:
        label = LabelWithPlaceholder(parent)
        if alignment is not None:
            label.setAlignment(alignment)
        label.setFont(font)

        width = label.sizeHint().width()
        height = label.sizeHint().height()
        if padding is not None:
            width += padding.getWidth(width)
            height += padding.getHeight(height)
        # self.lineEdit.selectionChanged.connect(lambda: self.lineEdit.setSelection(0, 0))
        # label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        label.setStyleSheet("background:transparent;border:none")
        return label

    def getThemeBuilder(self) -> ThemeBuilder:
        return LabelThemeBuilder()
