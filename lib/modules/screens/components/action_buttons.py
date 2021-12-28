from abc import ABC, abstractstaticmethod
from typing import Optional

from modules.screens.qss.qss_elements import Padding
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget
from widgets.action_button import QActionButton


class ViewActionButton(ABC):
    @abstractstaticmethod
    def render(font: QFont, padding: Padding, parent: Optional["QWidget"] = None):
        pass


class ActionButton(ViewActionButton):
    def render(font: QFont, padding: Padding = None, parent: Optional["QWidget"] = None):
        button = QActionButton(parent)
        button.setFont(font)
        button.setPadding(padding)
        return button
