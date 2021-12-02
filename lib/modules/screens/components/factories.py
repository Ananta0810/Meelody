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
    def getLabelByType(self, type: str) -> AbstractLabel:
        if type == "editable":
            return EditableLabel()
        return StandardLabel()


class SliderFactory:
    def getSliderByType(self, type: str) -> Slider:
        return HorizontalSlider()


class IconButtonFactory(ButtonFactory):
    def getButtonByType(self, type: str = None) -> Button:
        if type == "toggle":
            return ToggleIconButton()
        if type == "multiple-icon":
            return MultiIconButton()
        return IconButton()
