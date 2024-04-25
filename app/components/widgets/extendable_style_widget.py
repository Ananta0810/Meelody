from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget

from app.components.base import Component
from app.helpers.base import Strings


class ExtendableStyleWidget(QWidget, Component):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)

        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setAttribute(Qt.WA_Hover, True)
        self.setObjectName(Strings.randomId())
