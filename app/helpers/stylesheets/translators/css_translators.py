from typing import final

from app.helpers.stylesheets.translators.color_translator import ColorTranslator


@final
class CssTranslators:
    Color = ColorTranslator()
