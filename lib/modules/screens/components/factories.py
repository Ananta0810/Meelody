from abc import ABC, abstractmethod
from sys import path

from .icon_buttons import IconButton, MultiIconButton, ToggleIconButton
from .labels import EditableLabel, StandardLabel
from .sliders import HorizontalSlider

path.append(".\lib")
from modules.screens.components.view_item import ViewItem


class Factory(ABC):
    @abstractmethod
    def getByType(self, type: str) -> ViewItem:
        pass


class LabelFactory(Factory):
    _types = {
        "default": StandardLabel,
        "editable": EditableLabel,
    }

    def getByType(self, type: str) -> ViewItem:
        if type in self._types:
            return self._types.get(type)()
        raise ValueError("Factory doesn't support this type of label")


class SliderFactory(Factory):
    _types = {
        "horizontal": HorizontalSlider,
    }

    def getByType(self, type: str) -> ViewItem:
        if type in self._types:
            return self._types.get(type)()
        raise ValueError("Factory doesn't support this type of slider")


class IconButtonFactory(Factory):
    _types = {
        "default": IconButton,
        "toggle": ToggleIconButton,
        "multiple-icon": MultiIconButton,
    }

    def getByType(self, type: str = None) -> ViewItem:
        if type in self._types:
            return self._types.get(type)()
        raise ValueError("Factory doesn't support this type of button")
