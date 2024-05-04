from typing import Optional

from PyQt5.QtWidgets import QWidget

from app.helpers.base import Dicts, Strings, Lists
from app.helpers.stylesheets import Color
from app.helpers.stylesheets.translators.props_translators.class_name import ClassName
from app.helpers.stylesheets.translators.props_translators.props_translator import PropsTranslator
from app.helpers.stylesheets.translators.value_translators import ValueTranslators

_STYLES: set[str] = {"solid", "dotted", "dashed", "double", "hidden"}

_ALL_DIRECTIONS: str = "all"

_DIRECTIONS: dict[str, list[str]] = {
    "l": ["left"],
    "t": ["top"],
    "r": ["right"],
    "b": ["bottom"],
    "x": ["left", "right"],
    "y": ["top", "bottom"],
}

_NULL_DIRECTION_PROPS: list[str] = []


def _toProps(cn: ClassName) -> list[(Optional[str], str, int | str | Color)]:
    # border-t, border-x, border-b,...
    if cn.value in _DIRECTIONS:
        directions = _DIRECTIONS[cn.value]

        result = []
        for direction in directions:
            key, value = _toProps0(None)
            result.append((direction, key, value))
        return result

    # border-t-2, border-x-solid,....
    if cn.value is not None and "-" in cn.value:
        direction, props = cn.value.split("-", maxsplit=1)
        if direction in _DIRECTIONS:
            directions = _DIRECTIONS[direction]

            result = []
            for direction_ in directions:
                key, value = _toProps0(props)
                result.append((direction_, key, value))
            return result

    key, value = _toProps0(cn.value)
    return [(_ALL_DIRECTIONS, key, value)]


def _toProps0(value: Optional[str]) -> (str, int | str):
    if Strings.isBlank(value):
        return "size", 1

    if value.lower() == "none":
        return "size", 0

    if value.isdigit():
        return "size", int(value)

    if value in _STYLES:
        return "style", value

    return "color", ValueTranslators.Color.translate([value])


class BorderTranslator(PropsTranslator):
    __defaultSize: int = 1
    __defaultColor: str = Color(128, 128, 128).toStylesheet()
    __defaultStyle: str = "solid"

    def ids(self) -> set[str]:
        return {"border"}

    def translate(self, names: list[ClassName], target: QWidget) -> str:
        directions = Dicts.group(Lists.flat([_toProps(name) for name in names]), lambda prop: prop[0])

        generalProps = {key: value for direction, key, value in directions.get(_ALL_DIRECTIONS, _NULL_DIRECTION_PROPS)}

        size = generalProps.get('size', BorderTranslator.__defaultSize)
        color = generalProps.get('color', BorderTranslator.__defaultColor)
        style = generalProps.get('style', BorderTranslator.__defaultStyle)

        props = []

        if "size" in generalProps:
            props.append(f"border: {size}px {style} {color}")

        for direction, details in directions.items():
            if direction == _ALL_DIRECTIONS:
                continue

            directionProps = {key: value for direction, key, value in details}

            directionSize = directionProps.get('size', size)
            directionColor = directionProps.get('color', color)
            directionStyle = directionProps.get('style', style)

            props.append(f"border-{direction}: {directionSize}px {directionStyle} {directionColor}")

        return Strings.joinStyles(props)
