from modules.screens.themes.theme_builders import ButtonThemeBuilder, HorizontalSliderThemeBuilder, TextThemeBuilder

from .qss import Backgrounds, ColorBoxes


class IconButtonThemeBuilders:
    # =======================PRIMARY=======================
    CIRCLE_PRIMARY = ButtonThemeBuilder().addLightModeBackground(Backgrounds.CIRCLE_PRIMARY)
    CIRCLE_PRIMARY_25 = (
        ButtonThemeBuilder()
        .addLightModeBackground(Backgrounds.CIRCLE_PRIMARY_25)
        .addDarkModeBackground(Backgrounds.CIRCLE_WHITE_25)
    )
    CIRCLE_PRIMARY_DANGER_25 = (
        ButtonThemeBuilder()
        .addLightModeBackground(Backgrounds.CIRCLE_PRIMARY_25)
        .addDarkModeBackground(Backgrounds.CIRCLE_DANGER_25)
    )
    CIRCLE_HIDDEN_PRIMARY_DANGER_25 = (
        ButtonThemeBuilder()
        .addLightModeBackground(Backgrounds.CIRCLE_HIDDEN_PRIMARY_25)
        .addLightModeActiveBackground(Backgrounds.CIRCLE_HIDDEN_DANGER_25)
        .addDarkModeBackground(Backgrounds.CIRCLE_HIDDEN_WHITE_25)
        .addDarkModeActiveBackground(Backgrounds.CIRCLE_HIDDEN_DANGER_25)
    )
    CIRCLE_HIDDEN_PRIMARY_25 = (
        ButtonThemeBuilder()
        .addLightModeBackground(Backgrounds.CIRCLE_HIDDEN_PRIMARY_25)
        .addDarkModeBackground(Backgrounds.CIRCLE_HIDDEN_WHITE_25)
    )

    # =======================DANGER=======================
    CIRCLE_DANGER = ButtonThemeBuilder().addLightModeBackground(Backgrounds.CIRCLE_DANGER)


class TextThemeBuilders:
    DEFAULT = TextThemeBuilder().addLightModeTextColor(ColorBoxes.BLACK).addDarkModeTextColor(ColorBoxes.WHITE)
    GRAY = TextThemeBuilder().addLightModeTextColor(ColorBoxes.GRAY)

    BG_PRIMARY_25 = (
        TextThemeBuilder()
        .addLightModeTextColor(ColorBoxes.PRIMARY)
        .addLightModeBackground(Backgrounds.ROUNDED_PRIMARY_25)
        .addDarkModeTextColor(ColorBoxes.WHITE)
        .addDarkModeBackground(Backgrounds.ROUNDED_WHITE_25)
    )


class SliderThemeBuilders:
    PRIMARY = (
        HorizontalSliderThemeBuilder()
        .addLightHandleColor(ColorBoxes.PRIMARY)
        .addLightLineColor(ColorBoxes.HOVERABLE_PRIMARY_25)
        .addDarkLineColor(ColorBoxes.HOVERABLE_WHITE_25)
    )
    BG_PRIMARY = (
        HorizontalSliderThemeBuilder()
        .addLightHandleColor(ColorBoxes.PRIMARY)
        .addLightLineColor(ColorBoxes.HOVERABLE_PRIMARY_25)
        .addDarkLineColor(ColorBoxes.HOVERABLE_WHITE_25)
        .addLightModeBackground(Backgrounds.ROUNDED_PRIMARY_25)
        .addDarkModeBackground(Backgrounds.ROUNDED_WHITE_25)
    )
