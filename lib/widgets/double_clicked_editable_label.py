from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QLineEdit


class QDoubleClickedEditableLabel(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setReadOnly(True)
        self.lastInput: str = None
        self.defaultText = ""

    def mouseDoubleClickEvent(self, event):
        super().mouseDoubleClickEvent(event)
        self.setReadOnly(False)
        self.lastInput = self.text()

    def keyPressEvent(self, a0):
        super().keyPressEvent(a0)
        if a0.key() != Qt.Key_Return:
            return
        self.setReadOnly(True)

    def setDefaultText(self, text: str) -> None:
        if self.text() == self.defaultText:
            self.setText(text)
        self.defaultText = text

    def setText(self, text: str) -> None:
        text = self.defaultText if text is None else text
        super().setText(text)

    def isDisplayingDefaultText(self):
        return self.text() == self.defaultText
