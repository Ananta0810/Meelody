from modules.models.view.Color import Color
from modules.models.view.ColorBox import ColorBox


class Colors:
    PRIMARY = Color(128, 64, 255)

    SUCCESS = Color(50, 216, 100)
    DANGER = Color(255, 80, 80)
    WARNING = Color(255, 170, 28)

    WHITE = Color(255, 255, 255)
    BLACK = Color(0, 0, 0)
    GRAY = Color(128, 128, 128)
    TRANSPARENT = Color(255, 255, 255, 0)


class ColorBoxes:
    TRANSPARENT = ColorBox(Colors.TRANSPARENT)

    # =========================// Primary //=========================
    PRIMARY = ColorBox(Colors.PRIMARY)
    PRIMARY_75 = ColorBox(Colors.PRIMARY.with_opacity(75))
    PRIMARY_50 = ColorBox(Colors.PRIMARY.with_opacity(50))
    PRIMARY_25 = ColorBox(Colors.PRIMARY.with_opacity(25))

    # =========================// Warning //=========================
    WARNING = ColorBox(Colors.WARNING)
    WARNING_75 = ColorBox(Colors.WARNING.with_opacity(75))
    WARNING_50 = ColorBox(Colors.WARNING.with_opacity(50))
    WARNING_25 = ColorBox(Colors.WARNING.with_opacity(25))

    # =========================// Danger //=========================
    DANGER = ColorBox(Colors.DANGER)
    DANGER_75 = ColorBox(Colors.DANGER.with_opacity(75))
    DANGER_50 = ColorBox(Colors.DANGER.with_opacity(50))
    DANGER_25 = ColorBox(Colors.DANGER.with_opacity(25))

    # =========================// Black //=========================
    BLACK = ColorBox(Colors.BLACK)
    BLACK_75 = ColorBox(Colors.BLACK.with_opacity(75))
    BLACK_50 = ColorBox(Colors.BLACK.with_opacity(50))
    BLACK_25 = ColorBox(Colors.BLACK.with_opacity(25))

    # =========================// White //=========================
    WHITE = ColorBox(Colors.WHITE)
    WHITE_75 = ColorBox(Colors.WHITE.with_opacity(75))
    WHITE_50 = ColorBox(Colors.WHITE.with_opacity(50))
    WHITE_25 = ColorBox(Colors.WHITE.with_opacity(25))


class Backgrounds:
    pass
