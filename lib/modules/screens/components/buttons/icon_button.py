from sys import path

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton

from .button import Button

path.append(".lib/modules/")
from modules.screens.qss.qss_elements import QSSBackground, QSSPadding


class IconButton(Button):
    def render(
        self,
        icon: QIcon,
        iconSize: int,
        padding: QSSPadding,
        background: QSSBackground,
        parent=None,
    ) -> QPushButton:
        button = QPushButton(parent)
        button.setIcon(icon)
        button.setIconSize(iconSize)

        iconWidth = iconSize.width()
        buttonSize: int = iconWidth
        if padding is not None:
            buttonSize += padding.getWidth(iconWidth)
        button.setFixedSize(buttonSize, buttonSize)

        button.setStyleSheet(
            "QPushButton{"
            + f"padding: {padding.toStylesheet(size=buttonSize) if padding is not None else None};"
            + f"border:{background.borderStyleSheet()};"
            + f"border-radius:{background.borderRadiusStyleSheet(size=buttonSize)};"
            + f"background-color:{background.colorStyleSheet()};"
            + "}"
            + "QPushButton:hover{"
            + f"border:{background.borderStyleSheet(active=True)};"
            + f"background-color:{background.colorStyleSheet(active=True)};"
            + "}"
        )
        return button
