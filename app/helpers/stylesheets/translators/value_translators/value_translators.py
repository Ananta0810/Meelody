from typing import final

from app.helpers.stylesheets.translators.value_translators.color_translator import ColorTranslator


@final
class ValueTranslators:
    Color = ColorTranslator()
