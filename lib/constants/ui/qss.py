from modules.screens.qss.qss_elements import Color, ColorBox, Padding

from .metaclass import MetaConst


class Paddings(metaclass=MetaConst):
    RELATIVE_25 = Padding(0.25)
    RELATIVE_33 = Padding(0.33)
    RELATIVE_50 = Padding(0.5)
    RELATIVE_67 = Padding(0.67)
    RELATIVE_75 = Padding(0.75)
    RELATIVE_100 = Padding(1)

    ABSOLUTE_SMALL = Padding(4)
    ABSOLUTE_MEDIUM = Padding(12)


class Colors(metaclass=MetaConst):
    PRIMARY = Color(128, 64, 255)
    PRIMARY_DARK = Color(0, 0, 255)
    PRIMARY_LIGHT = Color(160, 160, 255)

    SUCCESS = Color(50, 216, 100)
    SUCCESS_DARK = Color(0, 192, 100)
    DANGER = Color(255, 80, 80)
    DANGER_DARK = Color(255, 0, 0)
    WARNING = Color(255, 170, 28)
    WARNING_DARK = Color(255, 128, 0)

    DISABLED = Color(128, 128, 128)
    white = Color(255, 255, 255)
    BLACK = Color(0, 0, 0)
    TRANSPARENT = Color(255, 255, 255, 0)


class ColorBoxes(metaclass=MetaConst):
    TRANSPARENT = ColorBox(Colors.TRANSPARENT)
    PRIMARY = ColorBox(Colors.PRIMARY)
    BLACK = ColorBox(Colors.BLACK)
    WHITE = ColorBox(Colors.white)
    GRAY = ColorBox(Colors.BLACK.withAlpha(0.5))
    DANGER = ColorBox(Colors.DANGER)

    BLACK_LIGHTEN = ColorBox(
        normal=Colors.BLACK.withAlpha(0.08),
        active=Colors.BLACK.withAlpha(0.12),
    )
    BLACK_LIGHTEN_50 = ColorBox(
        normal=Colors.BLACK.withAlpha(0.15),
        active=Colors.BLACK.withAlpha(0.25),
    )
    WHITE_LIGHTEN_25 = ColorBox(normal=Colors.white.withAlpha(0.15))
    WHITE_LIGHTEN_50 = ColorBox(normal=Colors.white.withAlpha(0.33))
    WHITE_LIGHTEN_HOVERABLE_25 = ColorBox(
        normal=Colors.white.withAlpha(0.15),
        active=Colors.white.withAlpha(0.25),
    )
    WHITE_LIGHTEN_HOVERABLE_50 = ColorBox(
        normal=Colors.white.withAlpha(0.33),
        active=Colors.white.withAlpha(0.5),
    )
    GRAY_LIGHTEN = ColorBox(
        normal=Colors.BLACK.withAlpha(0.4),
        active=Colors.BLACK.withAlpha(0.6),
    )
    PRIMARY_LIGHTEN_25 = ColorBox(normal=Colors.PRIMARY.withAlpha(0.15))
    PRIMARY_LIGHTEN_50 = ColorBox(normal=Colors.PRIMARY.withAlpha(0.33))
    PRIMARY_LIGHTEN_HOVERABLE_25 = ColorBox(
        normal=Colors.PRIMARY.withAlpha(0.15),
        active=Colors.PRIMARY.withAlpha(0.25),
    )
    PRIMARY_LIGHTEN_HOVERABLE_50 = ColorBox(
        normal=Colors.PRIMARY.withAlpha(0.33),
        active=Colors.PRIMARY.withAlpha(0.50),
    )
    SUCCESS = ColorBox(
        normal=Colors.SUCCESS.withAlpha(0.15),
        active=Colors.SUCCESS.withAlpha(0.25),
    )
    DANGER_LIGHTEN = ColorBox(
        normal=Colors.DANGER.withAlpha(0.15),
        active=Colors.DANGER.withAlpha(0.25),
    )
    DANGER_LIGHTEN_50 = ColorBox(
        normal=Colors.DANGER.withAlpha(0.33),
        active=Colors.DANGER.withAlpha(0.50),
    )
    WARNING = ColorBox(
        normal=Colors.WARNING.withAlpha(0.15),
        active=Colors.WARNING.withAlpha(0.25),
    )
    DISABLED = ColorBox(
        normal=Colors.DISABLED.withAlpha(0.15),
        active=Colors.DISABLED.withAlpha(0.25),
    )
    HIDDEN_PRIMARY = ColorBox(
        normal=Colors.TRANSPARENT,
        active=Colors.PRIMARY.withAlpha(0.15),
    )
    HIDDEN_SUCCESS = ColorBox(
        normal=Colors.TRANSPARENT,
        active=Colors.SUCCESS.withAlpha(0.15),
    )
    HIDDEN_DANGER = ColorBox(
        normal=Colors.TRANSPARENT,
        active=Colors.DANGER.withAlpha(0.15),
    )
    HIDDEN_WARNING = ColorBox(
        normal=Colors.TRANSPARENT,
        active=Colors.WARNING.withAlpha(0.15),
    )
    HIDDEN_WHITE = ColorBox(
        normal=Colors.TRANSPARENT,
        active=Colors.white.withAlpha(0.15),
    )
