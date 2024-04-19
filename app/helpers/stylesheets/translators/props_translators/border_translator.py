from typing import List

from app.helpers.base import Dicts
from app.helpers.stylesheets import Border, Color
from app.helpers.stylesheets.translators.props_translators.props_translator import PropsTranslator
from app.helpers.stylesheets.translators.value_translators.color_translator import ColorTranslator


def _toProps(name: str):
    parts = name.split("-")
    if len(parts) == 1:
        return "size", 1

    if parts[1].isdigit():
        return "size", int(parts[1])

    if len(parts) == 2:
        return "style", parts[2]

    color = parts[1:]
    translator = ColorTranslator()
    return "color", translator.translate(color)


class BorderTranslator(PropsTranslator[Border]):
    __defaultSize = 1
    __defaultColor = Color(128, 128, 128)
    __defaultStyle = "solid"

    def id(self) -> str:
        return "border"

    def translate(self, names: List[str]) -> Border:
        dictionary = dict([_toProps(name) for name in names])
        return Border(Dicts.getFrom(dictionary, 'size', otherwise=BorderTranslator.__defaultSize),
                      Dicts.getFrom(dictionary, 'color', otherwise=BorderTranslator.__defaultColor),
                      Dicts.getFrom(dictionary, 'style', otherwise=BorderTranslator.__defaultStyle))
