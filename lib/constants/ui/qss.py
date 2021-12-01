from sys import path

from .colors import Colors

path.append(".")
from lib.modules.screens.qss.qss_elements import *


class QSSPaddings:
    RELATIVE_25 = QSSPadding(0.25)
    RELATIVE_50 = QSSPadding(0.5)
    RELATIVE_75 = QSSPadding(0.75)
    RELATIVE_100 = QSSPadding(1)

    ABSOLUTE_MEDIUM = QSSPadding(12)


class QSSColors:
    FLAT_PRIMARY = QSSColor(normal=Colors.PRIMARY)
    BLACK = QSSColor(
        normal=Colors.BLACK.withAlpha(0.08),
        active=Colors.BLACK.withAlpha(0.12),
    )
    PRIMARY = QSSColor(
        normal=Colors.PRIMARY.withAlpha(0.15),
        active=Colors.PRIMARY.withAlpha(0.25),
    )
    SUCCESS = QSSColor(
        normal=Colors.SUCCESS.withAlpha(0.15),
        active=Colors.SUCCESS.withAlpha(0.25),
    )
    DANGER = QSSColor(
        normal=Colors.DANGER.withAlpha(0.15),
        active=Colors.DANGER.withAlpha(0.25),
    )
    WARNING = QSSColor(
        normal=Colors.WARNING.withAlpha(0.15),
        active=Colors.WARNING.withAlpha(0.25),
    )
    DISABLED = QSSColor(
        normal=Colors.DISABLED.withAlpha(0.15),
        active=Colors.DISABLED.withAlpha(0.25),
    )
    HIDDEN_PRIMARY = QSSColor(
        normal=Colors.TRANSPARENT,
        active=Colors.PRIMARY.withAlpha(0.15),
    )
    HIDDEN_SUCCESS = QSSColor(
        normal=Colors.TRANSPARENT,
        active=Colors.SUCCESS.withAlpha(0.15),
    )
    HIDDEN_DANGER = QSSColor(
        normal=Colors.TRANSPARENT,
        active=Colors.DANGER.withAlpha(0.15),
    )
    HIDDEN_WARNING = QSSColor(
        normal=Colors.TRANSPARENT,
        active=Colors.WARNING.withAlpha(0.15),
    )
