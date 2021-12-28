from PyQt5.QtWidgets import QLabel


class QLabelWithDefaultText(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.defaultText = ""

    def setDefaultText(self, text: str) -> None:
        if self.text() == self.defaultText:
            self.setText(text)
        self.defaultText = text

    def setText(self, text: str) -> None:
        text = self.defaultText if text is None else text
        return super().setText(text)
