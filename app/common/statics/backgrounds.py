from typing import final

from app.common.statics.colors import Colors
from app.helpers.stylesheets.background import Background


@final
class Backgrounds:
    none = Background(color=Colors.none)
    primary = Background(color=Colors.primary)
    success = Background(color=Colors.success)
    danger = Background(color=Colors.danger)
    warning = Background(color=Colors.warning)
    white = Background(color=Colors.white)
    black = Background(color=Colors.black)
    gray = Background(color=Colors.gray)
