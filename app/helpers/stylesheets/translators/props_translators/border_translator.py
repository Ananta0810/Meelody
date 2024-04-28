from PyQt5.QtWidgets import QWidget

from app.helpers.stylesheets import Color
from app.helpers.stylesheets.translators.props_translators.class_name import ClassName
from app.helpers.stylesheets.translators.props_translators.props_translator import PropsTranslator
from app.helpers.stylesheets.translators.value_translators import ValueTranslators

__STYLES = {"solid", "dotted", "dashed", "double", "hidden"}


def _toProps(cn: ClassName):
    if cn.value is None or cn.value.lower() == "none":
        return "size", 0

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

    def translate(self, names: list[ClassName], target: QWidget) -> str:
        dictionary = dict([_toProps(name) for name in names])

        size = dictionary.get('size', BorderTranslator.__defaultSize)
        color = dictionary.get('color', BorderTranslator.__defaultColor)
        style = dictionary.get('style', BorderTranslator.__defaultStyle)

        return f"border: {size}px {style} {color.toStylesheet()}"
