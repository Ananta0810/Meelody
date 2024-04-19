from typing import final

from app.helpers.stylesheets.translators.props_translators.background_translator import BackgroundTranslator
from app.helpers.stylesheets.translators.props_translators.border_translator import BorderTranslator


@final
class PropsTranslators:
    Border = BorderTranslator()
    Background = BackgroundTranslator()
