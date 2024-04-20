from typing import final

from app.helpers.stylesheets.translators.props_translators.background_translator import BackgroundTranslator
from app.helpers.stylesheets.translators.props_translators.border_translator import BorderTranslator
from app.helpers.stylesheets.translators.props_translators.rounded_translator import RoundedTranslator


@final
class PropsTranslators:
    Border = BorderTranslator()
    Background = BackgroundTranslator()
    Rounded = RoundedTranslator()
    Translators = [Border, Background, Rounded]
