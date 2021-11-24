from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QPushButton

from .background_color import BackgroundColor
from .button import Button
from .icon import Icon
from .toggle_button import ToggleButton


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

    def export(
        self,
        name: str,
        padding: float,
        iconSize: int,
        icon: Icon,
        checkedIcon: Icon = None,
        cursor: QCursor = None,
        parent=None,
    ) -> QPushButton:
        button = ToggleButton(parent)

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
        button.setObjectName(name)
        return button
