from sys import path

from PyQt5.QtGui import QCursor, QIcon
from PyQt5.QtWidgets import QPushButton

from .button import Button

path.append(".")
from lib.modules.screens.background_color import BackgroundColor
from lib.widgets.toggle_icon_button import QToggleButton


class ToggleIconButton(Button):
    def __init__(
        self,
        roundness: float = 0.5,
        padding: float = 0.5,
        border: str = "none",
        backgroundColor: BackgroundColor = None,
        checkedBackgroundColor: BackgroundColor = None,
    ):
        Button.__init__(self, roundness, border, backgroundColor)
        self.padding = padding
        self.checkedBackgroundColor = (
            checkedBackgroundColor
            if checkedBackgroundColor is not None
            else backgroundColor
        )

    def withBackground(
        self,
        backgroundColor: BackgroundColor,
        checkedBackground: BackgroundColor = None,
    ):
        self.backgroundColor = backgroundColor
        self.checkedBackgroundColor = (
            checkedBackground if checkedBackground is not None else backgroundColor
        )
        return self

    def export(
        self,
        padding: float,
        iconSize: int,
        icon: QIcon,
        checkedIcon: QIcon = None,
        cursor: QCursor = None,
        parent=None,
    ) -> QPushButton:
        button = QToggleButton(parent)

        button.setIcon(icon)
        button.setIconSize(iconSize)
        button.setNormalIcon(icon)
        button.setCheckedIcon(checkedIcon)
        button.setCheckable(True)
        button.setChecked(False)

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
            + "QPushButton:checked{"
            + f"background-color:{str(self.checkedBackgroundColor.normal) if self.checkedBackgroundColor is not None else None};"
            + "}"
            "QPushButton:hover:checked{"
            + f"background-color:{str(self.checkedBackgroundColor.hover) if self.checkedBackgroundColor is not None else None};"
            + "}"
        )
        return button
