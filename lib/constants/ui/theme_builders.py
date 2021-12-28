from modules.screens.themes.theme_builders import ButtonThemeBuilder, TextThemeBuilder

from .qss import Backgrounds, ColorBoxes


class IconButtonThemeBuilders:
    PRIMARY = (
        ButtonThemeBuilder()
        .addLightModeBackground(Backgrounds.CIRCLE_PRIMARY_25)
        .addDarkModeBackground(Backgrounds.CIRCLE_WHITE_25)
    )

    HIDDEN_PRIMARY = (
        ButtonThemeBuilder()
        .addLightModeBackground(Backgrounds.CIRCLE_HIDDEN_PRIMARY_25)
        .addDarkModeBackground(Backgrounds.CIRCLE_HIDDEN_WHITE_25)
    )

    DANGER = ButtonThemeBuilder().addLightModeBackground(Backgrounds.CIRCLE_DANGER)


class TextThemeBuilers:
    DEFAULT = TextThemeBuilder().addLightModeTextColor(ColorBoxes.BLACK).addDarkModeTextColor(ColorBoxes.WHITE)
    GRAY = TextThemeBuilder().addLightModeTextColor(ColorBoxes.GRAY)
