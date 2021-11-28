from sys import path

from PyQt5.QtGui import QCursor, QIcon
from PyQt5.QtWidgets import QPushButton

from .button import Button

path.append(".")
from lib.modules.screens.background_color import BackgroundColor


class IconButton(Button):
    def __init__(
        self,
        roundness: float = 0.5,
        border: str = "none",
        backgroundColor: BackgroundColor = None,
    ):
        Button.__init__(self, roundness, border, backgroundColor)

    def export(
        self,
        iconSize: int,
        icon: QIcon,
        cursor: QCursor = None,
        padding: float = 0.5,
        parent=None,
    ) -> QPushButton:
        button = QPushButton()

        button.setIcon(icon)
        button.setIconSize(iconSize)

        if cursor is not None:
            button.setCursor(cursor)

        padding = padding if padding > 1 else iconSize.width() * padding
        button.setFixedSize(iconSize.width() + padding, iconSize.width() + padding)

        borderRadius = (
            self.roundness
            if self.roundness >= 1
            else (iconSize.width() + padding) * self.roundness
        )
        button.setStyleSheet(
            "QPushButton{"
            + f"padding: {padding}px;"
            + f"border:{self.border};"
            + f"border-radius:{borderRadius};"
            + f"background-color:{str(self.backgroundColor.normal) if self.backgroundColor is not None else None};"
            + "}"
            + "QPushButton:hover{"
            + f"background-color:{str(self.backgroundColor.hover) if self.backgroundColor is not None else None};"
            + "}"
        )
        return button
