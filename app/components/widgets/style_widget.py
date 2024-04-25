from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget

from app.components.base import Component
from app.helpers.base import Strings


class StyleWidget(QWidget, Component):

    def __init__(self, parent: Optional[QWidget] = None):
        super(StyleWidget, self).__init__(parent)
        self.__initUI()
        self.setObjectName(Strings.randomId())

    def __initUI(self) -> None:
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setAttribute(Qt.WA_Hover, True)
