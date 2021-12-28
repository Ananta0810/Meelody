from typing import Optional

from modules.screens.qss.qss_elements import Padding
from PyQt5.QtWidgets import QPushButton, QWidget


class QActionButton(QPushButton):
    padding: Padding

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.padding = None

    def setPadding(self, padding: Padding) -> None:
        self.padding = padding

    def setText(self, text: str) -> None:
        super().setText(text)
        self.paddingText()

    def paddingText(self) -> None:
        if self.padding is None:
            return
        textSize = self.sizeHint()
        self.setFixedSize(
            textSize.width() + self.padding.getWidth(textSize.width()),
            textSize.height() + self.padding.getHeight(textSize.height()),
        )
