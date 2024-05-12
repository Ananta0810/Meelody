from typing import Optional

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLineEdit, QWidget

from app.components.base import Component


class Input(QLineEdit, Component):
    changed: pyqtSignal = pyqtSignal(str)

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        super()._initComponent()

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        self.changed.emit(self.text())
