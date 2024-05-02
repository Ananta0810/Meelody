from typing import Optional

from PyQt5.QtWidgets import QWidget

from app.helpers.base import Dicts, Strings
from app.helpers.stylesheets import Color
from app.helpers.stylesheets.translators.props_translators.class_name import ClassName
from app.helpers.stylesheets.translators.props_translators.props_translator import PropsTranslator
from app.helpers.stylesheets.translators.value_translators import ValueTranslators

_STYLES = {"solid", "dotted", "dashed", "double", "hidden"}
_DIRECTIONS = {"l": "left", "t": "top", "r": "right", "b": "bottom"}
_NULL_DIRECTION_PROPS = []
_ALL_DIRECTIONS = "all"


def _toProps(cn: ClassName) -> (Optional[str], str, int | str | Color):
    if "-" in cn.value:
        direction, props = cn.value.split("-", maxsplit=1)
        if direction in _DIRECTIONS:
            key, value = _toProps0(props)
            return direction, key, value

    key, value = _toProps0(cn.value)
    return _ALL_DIRECTIONS, key, value


def _toProps0(value: str) -> (str, int | str | Color):
    if value is None or value.lower() == "none":
        return "size", 0

    if value.isdigit():
        return "size", int(value)

    if value in _STYLES:
        return "style", value

    return "color", ValueTranslators.Color.translate([value])


class BorderTranslator(PropsTranslator):
    __defaultSize = 1
    __defaultColor = Color(128, 128, 128)
    __defaultStyle = "solid"

    def ids(self) -> set[str]:
        return {"border"}

    def translate(self, names: list[ClassName], target: QWidget) -> str:
        directions = Dicts.group([_toProps(name) for name in names], lambda prop: prop[0])

        generalProps = {key: value for direction, key, value in directions.get(_ALL_DIRECTIONS, _NULL_DIRECTION_PROPS)}

        size = generalProps.get('size', BorderTranslator.__defaultSize)
        color = generalProps.get('color', BorderTranslator.__defaultColor)
        style = generalProps.get('style', BorderTranslator.__defaultStyle)

        props = [f"border: {size}px {style} {color.toStylesheet()}"]

        for direction, details in directions.items():
            if direction == _ALL_DIRECTIONS:
                continue

            directionProps = {key: value for direction, key, value in details}

            directionSize = directionProps.get('size', BorderTranslator.__defaultSize)
            directionColor = directionProps.get('color', BorderTranslator.__defaultColor)
            directionStyle = directionProps.get('style', BorderTranslator.__defaultStyle)

            props.append(f"border-{_DIRECTIONS[direction]}: {directionSize}px {directionStyle} {directionColor.toStylesheet()}")

        return Strings.joinStyles(props)
