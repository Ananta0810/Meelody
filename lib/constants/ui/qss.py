from sys import path

from .metaclass import MetaConst

path.append(".")
from lib.modules.screens.qss.qss_elements import *


class Paddings(metaclass=MetaConst):
    RELATIVE_25 = QSSPadding(0.25)
    RELATIVE_50 = QSSPadding(0.5)
    RELATIVE_75 = QSSPadding(0.75)
    RELATIVE_100 = QSSPadding(1)

    ABSOLUTE_MEDIUM = QSSPadding(12)


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
    WHITE = Color(255, 255, 255)
    BLACK = Color(0, 0, 0)
    TRANSPARENT = Color(255, 255, 255, 0)


class ColorBoxes(metaclass=MetaConst):
    FLAT_PRIMARY = ColorBox(Colors.PRIMARY)
    FLAT_GRAY = ColorBox(Colors.BLACK.withAlpha(0.5))
    BLACK = ColorBox(
        normal=Colors.BLACK.withAlpha(0.08),
        active=Colors.BLACK.withAlpha(0.12),
    )
    GRAY = ColorBox(
        normal=Colors.BLACK.withAlpha(0.4),
        active=Colors.BLACK.withAlpha(0.6),
    )
    PRIMARY = ColorBox(
        normal=Colors.PRIMARY.withAlpha(0.15),
        active=Colors.PRIMARY.withAlpha(0.25),
    )
    SUCCESS = ColorBox(
        normal=Colors.SUCCESS.withAlpha(0.15),
        active=Colors.SUCCESS.withAlpha(0.25),
    )
    DANGER = ColorBox(
        normal=Colors.DANGER.withAlpha(0.15),
        active=Colors.DANGER.withAlpha(0.25),
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
