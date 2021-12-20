from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QLineEdit


class QDoubleClickedEditableLabel(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setReadOnly(True)
        self.lastInput: str = None

    def mouseDoubleClickEvent(self, event):
        super().mouseDoubleClickEvent(event)
        self.setReadOnly(False)
        self.lastInput = self.text()

    def keyPressEvent(self, a0):
        super().keyPressEvent(a0)
        if a0.key() != Qt.Key_Return:
            return
        self.setReadOnly(True)
