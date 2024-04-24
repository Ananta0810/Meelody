from typing import final

from app.helpers.stylesheets.translators.props_translators.background_translator import BackgroundTranslator
from app.helpers.stylesheets.translators.props_translators.border_translator import BorderTranslator
from app.helpers.stylesheets.translators.props_translators.rounded_translator import RoundedTranslator
from app.helpers.stylesheets.translators.props_translators.text_translator import TextTranslator


@final
class PropsTranslators:
    Border = BorderTranslator()
    Background = BackgroundTranslator()
    Rounded = RoundedTranslator()
    Text = TextTranslator()
    Translators = [Border, Background, Rounded, Text]
