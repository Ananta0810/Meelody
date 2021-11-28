from sys import path

path.append(".")
from lib.modules.models.color import Color


class Colors:
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
