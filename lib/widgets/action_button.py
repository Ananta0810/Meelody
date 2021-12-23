from typing import Optional

from modules.screens.qss.qss_elements import Padding
from PyQt5.QtWidgets import QPushButton, QWidget


class QActionButton(QPushButton):
    padding: Padding

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.padding = None
        self.textChanged.connect(self.paddingText)

    def setPadding(self, padding: Padding) -> None:
        self.padding = padding

    def paddingText(self) -> None:
        if self.padding is None:
            return
        textSize = self.sizeHint()
        self.setBaseSize(
            textSize.width() + self.padding.getWidth(textSize.width()),
            textSize.height() + self.padding.getHeight(textSize.height()),
        )
