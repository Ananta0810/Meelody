from app.helpers.stylesheets import StylesheetProps
from app.helpers.stylesheets.translators import CssTranslators


class ClassNameTranslator:
    @staticmethod
    def translate(classNames: str) -> StylesheetProps:
        return CssTranslators.Border.translate([name for name in classNames.split(" ") if CssTranslators.Border.id()])
