from typing import Optional

from PyQt5.QtWidgets import QWidget, QPushButton

from app.common.statics.qt import Cursors
from app.components.base.base_component import Component


class ActionButton(QPushButton, Component):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        super()._initComponent()

    def _createUI(self) -> None:
        self.setCursor(Cursors.pointer)
