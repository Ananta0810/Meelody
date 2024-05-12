from PyQt5.QtWidgets import QWidget

from app.helpers.stylesheets.translators.props_translators.class_name import ClassName
from app.helpers.stylesheets.translators.props_translators.props_translator import PropsTranslator
from app.utils.base import Lists

__SIZES: dict[str, int] = {
    "sm": 2,
    "md": 4,
    "lg": 8,
    "xl": 16,
    "2xl": 32
}

_BASE: str = "base"

_TOP_LEFT: str = "tl"
_TOP_RIGHT: str = "tr"
_BOTTOM_RIGHT: str = "br"
_BOTTOM_LEFT: str = "bl"

_CORNERS: set[str] = {_TOP_LEFT, _TOP_RIGHT, _BOTTOM_RIGHT, _BOTTOM_LEFT}

_DIRECTIONS: dict[str, list[str]] = {
    "l": [_TOP_LEFT, _BOTTOM_LEFT],
    "t": [_TOP_LEFT, _TOP_RIGHT],
    "r": [_TOP_RIGHT, _BOTTOM_RIGHT],
    "b": [_BOTTOM_RIGHT, _BOTTOM_LEFT]
}


def _toProps(cn: ClassName, target: QWidget) -> list[(str, int | float)]:
    if "-" in cn.value:
        direction, props = cn.value.split("-", maxsplit=1)

        if direction in _CORNERS:
            value = _toDirectionProps(props, target)
            return [(direction, value)]

        if direction in _DIRECTIONS:
            corners = _DIRECTIONS[direction]
            return [(corner, _toDirectionProps(props, target)) for corner in corners]

    return [(_BASE, _toDirectionProps(cn.value, target))]


def _toDirectionProps(value: str, target: QWidget) -> int | float:
    if value is None:
        raise ValueError("Please add value to rounded")

    if value == "none":
        return 0

    if value == "full":
        smallerEdge = min(target.width(), target.height())
        return smallerEdge / 2

    if value in __SIZES:
        return __SIZES[value]

    if "/" in value:
        smallerEdge = min(target.width(), target.height())
        return smallerEdge * float(value)

    return float(value)


class RoundedTranslator(PropsTranslator):

    def ids(self) -> set[str]:
        return {"rounded"}

    def translate(self, names: list[ClassName], target: QWidget) -> str:
        dictionary = {k: v for k, v in Lists.flat([_toProps(cn, target) for cn in names])}

        base = dictionary.get(_BASE, 0)

        if len(dictionary) == 1 and _BASE in dictionary:
            return f"border-radius: {base}px"

        tl = dictionary.get(_TOP_LEFT, base)
        tr = dictionary.get(_TOP_RIGHT, base)
        br = dictionary.get(_BOTTOM_RIGHT, base)
        bl = dictionary.get(_BOTTOM_LEFT, base)

        return f"""
            border-top-left-radius :{tl}px;
            border-top-right-radius : {tr}px; 
            border-bottom-left-radius : {br}px; 
            border-bottom-right-radius : {bl}px
        """
