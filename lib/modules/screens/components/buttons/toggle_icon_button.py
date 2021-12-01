from sys import path

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton

from .button import Button

path.append("./lib")
from modules.screens.qss.qss_elements import QSSBackground, QSSPadding
from widgets.toggle_icon_button import QToggleButton


class ToggleIconButton(Button):
    def render(
        self,
        iconSize: int,
        icon: QIcon,
        checkedIcon: QIcon,
        padding: QSSPadding,
        background: QSSBackground,
        checkedBackground: QSSBackground = None,
        parent=None,
    ) -> QPushButton:
        button = QToggleButton(parent)

        button.setIcon(icon)
        button.setIconSize(iconSize)
        button.setNormalIcon(icon)
        button.setCheckedIcon(checkedIcon)
        button.setCheckable(True)

        iconWidth = iconSize.width()
        buttonSize: int = iconWidth + padding.getWidth(iconWidth)
        button.setFixedSize(buttonSize, buttonSize)

        styleSheet = (
            "QPushButton{"
            + f"padding: {padding.toStylesheet(size=buttonSize)};"
            + f"border:{background.borderStyleSheet()};"
            + f"border-radius:{background.borderRadiusStyleSheet(size=buttonSize)};"
            + f"background-color:{background.colorStyleSheet()};"
            + "}"
            + "QPushButton:hover{"
            + f"border:{background.borderStyleSheet(active=True)};"
            + f"background-color:{background.colorStyleSheet(active=True)};"
            + "}"
        )
        if checkedBackground is not None:
            styleSheet += (
                "QPushButton:checked{"
                + f"border:{checkedBackground.borderStyleSheet()};"
                + f"border-radius:{checkedBackground.borderRadiusStyleSheet(size=buttonSize)};"
                + f"background-color:{checkedBackground.colorStyleSheet()};"
                + "}"
                "QPushButton:hover:checked{"
                + f"border:{checkedBackground.borderStyleSheet(active=True)};"
                + f"background-color:{checkedBackground.colorStyleSheet(active=True)};"
                + "}"
            )
        button.setStyleSheet(styleSheet)
        return button
