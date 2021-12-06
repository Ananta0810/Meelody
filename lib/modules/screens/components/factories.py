from .buttons.button import Button
from .buttons.factory import ButtonFactory
from .buttons.icon_button import IconButton
from .buttons.multiple_icon_button import MultiIconButton
from .buttons.toggle_icon_button import ToggleIconButton
from .slider.horizontal_slider import HorizontalSlider
from .slider.slider import Slider
from .text.abstract_text import AbstractLabel
from .text.editable_label import EditableLabel
from .text.standard_label import StandardLabel


class LabelFactory:
    _types = {
        "default": StandardLabel,
        "editable": EditableLabel,
    }

    def getLabelByType(self, type: str) -> AbstractLabel:
        if type in self._types:
            return self._types.get(type)()
        raise ValueError("Factory doesn't support this type of label")


class SliderFactory:
    _types = {
        "horizontal": HorizontalSlider,
    }

    def getSliderByType(self, type: str) -> Slider:
        if type in self._types:
            return self._types.get(type)()
        raise ValueError("Factory doesn't support this type of slider")


class IconButtonFactory(ButtonFactory):
    _types = {
        "default": IconButton,
        "toggle": ToggleIconButton,
        "multiple-icon": MultiIconButton,
    }

    def getButtonByType(self, type: str = None) -> Button:
        if type in self._types:
            return self._types.get(type)()
        raise ValueError("Factory doesn't support this type of button")
