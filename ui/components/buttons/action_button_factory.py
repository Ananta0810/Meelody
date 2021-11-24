from sys import path

path.append(".")
from PyQt5.QtWidgets import QPushButton
from ui.base.colors import Colors

from .action_button import ActionButton
from .background_color import BackgroundColor
from .factory import ButtonFactory


class ActionButtonFactory(ButtonFactory):
    def __init__(self):
        self.buttons: dict = {
            "primary": ActionButton(
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
                textColor=Colors.DISABLED,
                backgroundColor=BackgroundColor(
                    normal=Colors.DISABLED.withAlpha(0.25),
                    hover=Colors.DISABLED.withAlpha(0.25),
                ),
            ),
            "success": ActionButton(
                textColor=Colors.WHITE,
                backgroundColor=BackgroundColor(
                    normal=Colors.SUCCESS,
                    hover=Colors.SUCCESS_DARK,
                ),
            ),
            "danger": ActionButton(
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
            "outlined-primary": ActionButton(
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
