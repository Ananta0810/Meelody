from sys import path

from PyQt5.QtWidgets import QPushButton

from .action_button import ActionButton
from .factory import ButtonFactory

path.append("./lib")

from constants.ui.colors import Colors


class ActionButtonFactory(ButtonFactory):
    def __init__(self):
        self.buttons: dict = {
            "PRIMARY": ActionButton(
                textColor=Colors.WHITE,
                backgroundColor=BackgroundColor(
                    normal=Colors.PRIMARY,
                    hover=Colors.PRIMARY_DARK,
                ),
            ),
            "secondary": ActionButton(
                textColor=Colors.PRIMARY,
                backgroundColor=BackgroundColor(
                    normal=Colors.PRIMARY.withAlpha(0.15),
                    hover=Colors.PRIMARY_DARK.withAlpha(0.25),
                ),
            ),
            "disabled": ActionButton(
                textColor=Colors.GRAY,
                backgroundColor=BackgroundColor(
                    normal=Colors.GRAY.withAlpha(0.25),
                    hover=Colors.GRAY.withAlpha(0.25),
                ),
            ),
            "SUCCESS": ActionButton(
                textColor=Colors.WHITE,
                backgroundColor=BackgroundColor(
                    normal=Colors.SUCCESS,
                    hover=Colors.SUCCESS_DARK,
                ),
            ),
            "DANGER": ActionButton(
                textColor=Colors.WHITE,
                backgroundColor=BackgroundColor(
                    normal=Colors.DANGER,
                    hover=Colors.DANGER_DARK,
                ),
            ),
            "warning": ActionButton(
                textColor=Colors.WHITE,
                backgroundColor=BackgroundColor(
                    normal=Colors.WARNING,
                    hover=Colors.WARNING_DARK,
                ),
            ),
            "outlined-PRIMARY": ActionButton(
                backgroundColor=BackgroundColor(
                    normal=Colors.TRANSPARENT,
                    hover=Colors.PRIMARY,
                ),
                border=f"2px solid {Colors.PRIMARY}",
                textColor=Colors.PRIMARY,
                textHoverColor=Colors.WHITE,
            ),
        }

    def createButton(
        self,
        type: str,
        name: str,
        text: str,
        font: str,
        cursor=None,
        parent=None,
    ) -> QPushButton:
        if not type in self.buttons:
            return None
        return self.buttons[type].export(name, text, font, cursor, parent)
