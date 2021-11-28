from sys import path

from PyQt5.QtWidgets import QPushButton, QSizePolicy

from .button import Button

path.append("./lib/modules/")

from models.color import Color
from screens.background_color import BackgroundColor


class ActionButton(Button):
    def __init__(
        self,
        backgroundColor: BackgroundColor = None,
        roundness: float = 12.0,
        padding: str = "1em 2em",
        text: str = "",
        textColor: Color = None,
        textHoverColor: Color = None,
        border: str = "none",
    ):
        Button.__init__(self, roundness, border, backgroundColor)
        self.padding = padding
        self.text = text
        self.textColor = textColor
        self.textHoverColor = (
            textHoverColor if textHoverColor is not None else textColor
        )

    def export(
        self,
        name: str,
        text: str,
        font,
        cursor,
        parent=None,
    ) -> QPushButton:

        button = QPushButton(parent)
        button.setSizePolicy(
            QSizePolicy.Preferred,
            QSizePolicy.Expanding,
        )

        button.setText(text)
        button.setFont(font)
        button.setStyleSheet(
            "QPushButton{"
            + f"padding: {self.padding};"
            + f"border:{self.border};"
            + f"border-radius:{self.roundness};"
            + f"background-color:{str(self.backgroundColor.normal)};"
            + f"color: {str(self.textColor)};"
            + "}"
            + "QPushButton:Hover{"
            + f"background-color:{str(self.backgroundColor.hover)};"
            + f"color: {str(self.textHoverColor)};"
            + "}"
        )
        if cursor is not None:
            button.setCursor(cursor)
        button.setFixedSize(button.sizeHint().width(), button.sizeHint().height())
        button.setObjectName(name)
        return button
