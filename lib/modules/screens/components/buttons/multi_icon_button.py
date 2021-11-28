from sys import path

from PyQt5.QtGui import QCursor, QIcon
from PyQt5.QtWidgets import QPushButton

from .button import Button

path.append("./lib")
from modules.screens.background_color import BackgroundColor
from widgets.multiple_icon_button import QMultipleIconButton


class MultiIconButton(Button):
    def __init__(
        self,
        roundness: float = 0.5,
        padding: float = 0.5,
        border: str = "none",
        backgroundColor: BackgroundColor = None,
    ):
        Button.__init__(self, roundness, border, backgroundColor)
        self.padding = padding

    def withBackground(self, backgroundColor: BackgroundColor):
        self.backgroundColor = backgroundColor
        return self

    def export(
        self,
        padding: float,
        iconSize: int,
        iconList: list[QIcon],
        cursor: QCursor = None,
        parent=None,
    ) -> QPushButton:
        button = QMultipleIconButton(parent)
        button.setIconSize(iconSize)
        button.setIconList(iconList)

        if cursor is not None:
            button.setCursor(cursor)
        if padding is not None:
            self.padding = padding

        padding = self.padding if self.padding > 1 else iconSize.width() * self.padding
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
