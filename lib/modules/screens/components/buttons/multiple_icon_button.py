from sys import path

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton

from .button import Button

path.append("./lib")
from modules.screens.qss.qss_elements import QSSBackground, QSSPadding
from widgets.multiple_icon_button import QMultipleIconButton


class MultiIconButton(Button):
    def render(
        self,
        icons: list[QIcon],
        iconSize: int,
        padding: QSSPadding = None,
        background: QSSBackground = None,
        parent=None,
    ) -> QPushButton:
        button = QMultipleIconButton(parent)
        button.setIconSize(iconSize)
        button.setIconList(icons)
        button.setCurrentIcon(0)

        iconWidth = iconSize.width()
        buttonSize: int = iconWidth
        if padding is not None:
            buttonSize += padding.getWidth(iconWidth)
        button.setFixedSize(buttonSize, buttonSize)

        styleSheet: str = (
            "QPushButton{"
            + f"padding:{padding.toStylesheet(size=buttonSize) if padding is not None else None};"
        )
        styleSheet += (
            "border:None}"
            if background is None
            else (
                f"border:{background.borderStyleSheet()};"
                + f"border-radius:{background.borderRadiusStyleSheet(size=buttonSize)};"
                + f"background-color:{background.colorStyleSheet()};"
                + "}"
                + "QPushButton:hover{"
                + f"border:{background.borderStyleSheet(active=True)};"
                + f"background-color:{background.colorStyleSheet(active=True)};"
                + "}"
            )
        )
        button.setStyleSheet(styleSheet)
        return button
