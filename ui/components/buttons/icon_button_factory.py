from sys import path

from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QPushButton

from .background_color import BackgroundColor
from .factory import ButtonFactory
from .icon import Icon
from .icon_button import IconButton
from .toggle_icon_button import ToggleIconButton

path.append(".")

from ui.base.colors import Colors


class IconButtonFactory(ButtonFactory):
    def __init__(self):
        self._standardButtons: dict = {
            "unstyled": IconButton(),
            "default": IconButton(
                backgroundColor=BackgroundColor(
                    normal=Colors.BLACK.withAlpha(0.15),
                    hover=Colors.BLACK.withAlpha(0.25),
                ),
            ),
            "primary": IconButton(
                backgroundColor=BackgroundColor(
                    normal=Colors.PRIMARY.withAlpha(0.15),
                    hover=Colors.PRIMARY.withAlpha(0.25),
                ),
            ),
            "success": IconButton(
                backgroundColor=BackgroundColor(
                    normal=Colors.SUCCESS.withAlpha(0.15),
                    hover=Colors.SUCCESS.withAlpha(0.25),
                ),
            ),
            "danger": IconButton(
                backgroundColor=BackgroundColor(
                    normal=Colors.DANGER.withAlpha(0.15),
                    hover=Colors.DANGER.withAlpha(0.25),
                ),
            ),
            "warning": IconButton(
                backgroundColor=BackgroundColor(
                    normal=Colors.WARNING.withAlpha(0.15),
                    hover=Colors.WARNING.withAlpha(0.25),
                ),
            ),
            "disabled": IconButton(
                backgroundColor=BackgroundColor(
                    normal=Colors.DISABLED.withAlpha(0.15),
                    hover=Colors.DISABLED.withAlpha(0.25),
                ),
            ),
            # Buttons transparent in normal mode
            "hidden-primary": IconButton(
                backgroundColor=BackgroundColor(
                    normal=Colors.TRANSPARENT,
                    hover=Colors.PRIMARY.withAlpha(0.15),
                ),
            ),
            "hidden-success": IconButton(
                backgroundColor=BackgroundColor(
                    normal=Colors.TRANSPARENT,
                    hover=Colors.SUCCESS.withAlpha(0.15),
                ),
            ),
            "hidden-danger": IconButton(
                backgroundColor=BackgroundColor(
                    normal=Colors.TRANSPARENT,
                    hover=Colors.DANGER.withAlpha(0.15),
                ),
            ),
            "hidden-warning": IconButton(
                backgroundColor=BackgroundColor(
                    normal=Colors.TRANSPARENT,
                    hover=Colors.WARNING.withAlpha(0.15),
                ),
            ),
            "hidden-disabled": IconButton(
                backgroundColor=BackgroundColor(
                    normal=Colors.TRANSPARENT,
                    hover=Colors.DISABLED.withAlpha(0.15),
                ),
            ),
            # Checkable buttons
        }

        self._toggleButtons: dict = {
            "primary-danger": ToggleIconButton(
                backgroundColor=BackgroundColor(
                    normal=Colors.PRIMARY.withAlpha(0.15),
                    hover=Colors.PRIMARY.withAlpha(0.25),
                ),
                checkedBackgroundColor=BackgroundColor(
                    normal=Colors.DANGER.withAlpha(0.15),
                    hover=Colors.DANGER.withAlpha(0.25),
                ),
            ),
            "hidden-primary": ToggleIconButton(
                backgroundColor=BackgroundColor(
                    normal=Colors.TRANSPARENT,
                    hover=Colors.PRIMARY.withAlpha(0.15),
                ),
            ),
            "hidden-primary-danger": ToggleIconButton(
                backgroundColor=BackgroundColor(
                    normal=Colors.TRANSPARENT,
                    hover=Colors.PRIMARY.withAlpha(0.15),
                ),
                checkedBackgroundColor=BackgroundColor(
                    normal=Colors.TRANSPARENT,
                    hover=Colors.DANGER.withAlpha(0.15),
                ),
            ),
        }

    def createButton(
        self,
        type: str,
        name: str,
        iconSize: int,
        icon: Icon,
        checkedIcon: Icon = None,
        cursor: QCursor = None,
        padding: float = None,
        parent=None,
    ) -> QPushButton:
        try:
            if "checkable-" in type:
                button = self._toggleButtons[type.replace("checkable-", "")]
                if padding is not None:
                    button.padding = padding
                return button.export(
                    name=name,
                    padding=padding,
                    iconSize=iconSize,
                    icon=icon,
                    checkedIcon=checkedIcon,
                    cursor=cursor,
                    parent=parent,
                )
            else:
                button = self._standardButtons[type]
                if padding is not None:
                    button.padding = padding
                return button.export(
                    name=name,
                    iconSize=iconSize,
                    icon=icon,
                    cursor=cursor,
                    parent=parent,
                )
        except:
            return None
