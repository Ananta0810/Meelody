from typing import final

from app.helpers.stylesheets.color import Color


@final
class Colors:
    primary = Color(100, 32, 255)
    success = Color(50, 216, 100)
    danger = Color(255, 80, 80)
    warning = Color(255, 170, 28)
    white = Color(255, 255, 255)
    dark = Color(32, 32, 32)
    black = Color(0, 0, 0)
    gray = Color(128, 128, 128)
    none = Color(255, 255, 255, 0)
