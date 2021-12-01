from .button import Button
from .factory import ButtonFactory
from .icon_button import IconButton
from .multiple_icon_button import MultiIconButton
from .toggle_icon_button import ToggleIconButton


class IconButtonFactory(ButtonFactory):
    def getButton(self, type: str = None) -> Button:
        if type == "toggle":
            return ToggleIconButton()
        if type == "multiple-icon":
            return MultiIconButton()
        return IconButton()
