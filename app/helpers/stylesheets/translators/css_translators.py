from typing import final

from app.helpers.stylesheets.translators.border_translator import BorderTranslator
from app.helpers.stylesheets.translators.color_translator import ColorTranslator


@final
class CssTranslators:
    Color = ColorTranslator()
    Border = BorderTranslator()
