from sys import path

from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QPushButton

from .button import Button
from .toggle_button import ToggleButton

path.append(".")
from ui.models.background_color import BackgroundColor
from ui.models.icon import Icon


class IconButton(Button):
    def __init__(
        self,
        roundness: float = 0.5,
        padding: float = 0.5,
        border: str = "none",
        backgroundColor: BackgroundColor = None,
    ):
        Button.__init__(self, roundness, border, backgroundColor)
        self.padding = padding

    def export(
        self,
        iconSize: int,
        icon: Icon,
        cursor: QCursor = None,
        parent=None,
    ) -> QPushButton:
        button = ToggleButton(parent)

        button.setIcon(icon)
        button.setIconSize(iconSize)
        button.setNormalIcon(icon)

        if cursor is not None:
            button.setCursor(cursor)

        padding = self.padding if self.padding > 1 else iconSize.width() * self.padding
        button.setFixedSize(iconSize.width() + padding, iconSize.width() + padding)

        borderRadius = (
            self.roundness
            if self.roundness >= 1
            else (iconSize.width() + padding) * self.roundness
        )
        stylesheet: str = (
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

        button.setStyleSheet(stylesheet)
        return button
