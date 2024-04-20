from typing import List

from PyQt5.QtWidgets import QWidget

from app.helpers.base import Dicts
from app.helpers.stylesheets import Color
from app.helpers.stylesheets.translators.props_translators.class_name import ClassName
from app.helpers.stylesheets.translators.props_translators.props_translator import PropsTranslator
from app.helpers.stylesheets.translators.value_translators import ValueTranslators

__STYLES = {"solid", "dotted", "dashed", "double", "hidden"}


def _toProps(cn: ClassName):
    if cn.value is None:
        return "size", 1

    if cn.value.isdigit():
        return "size", int(cn.value)

    if cn.value in __STYLES:
        return "style", cn.value

    return "color", ValueTranslators.Color.translate([cn.value])


class BorderTranslator(PropsTranslator):
    __defaultSize = 1
    __defaultColor = Color(128, 128, 128)
    __defaultStyle = "solid"

    def id(self) -> str:
        return "border"

    def translate(self, names: List[ClassName], target: QWidget) -> str:
        dictionary = dict([_toProps(name) for name in names])

        size = Dicts.getFrom(dictionary, 'size', otherwise=BorderTranslator.__defaultSize)
        color = Dicts.getFrom(dictionary, 'color', otherwise=BorderTranslator.__defaultColor)
        style = Dicts.getFrom(dictionary, 'style', otherwise=BorderTranslator.__defaultStyle)

        return f"border: {size}px {style} {color.toStylesheet()}"
