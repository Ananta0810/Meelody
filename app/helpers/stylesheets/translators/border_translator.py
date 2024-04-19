from typing import List

from app.helpers.stylesheets import Border, Color
from app.helpers.stylesheets.translators.color_translator import ColorTranslator


def get(key: str, dictionary: dict[str, any], defaultValue: any = None):
    return dictionary[key] if key in dictionary else defaultValue


class BorderTranslator:
    def id(self) -> str:
        return "border"

    def translate(self, names: List[str]):
        dictionary = dict([self._toProps(name) for name in names])
        return Border(get('size', dictionary, 1), get('color', dictionary, Color(128, 128, 128)),
                      get('style', dictionary, "solid"))

    def _toProps(self, name: str):
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
