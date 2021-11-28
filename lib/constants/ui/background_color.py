from sys import path

from .colors import Colors

path.append("./lib")

from modules.screens.background_color import BackgroundColor


class BackgroundColorSamples:
    def __init__(self):
        self.FLAT_PRIMARY = BackgroundColor(normal=Colors.PRIMARY)

        self.BLACK = BackgroundColor(
            normal=Colors.BLACK.withAlpha(0.15),
            hover=Colors.BLACK.withAlpha(0.25),
        )
        self.PRIMARY = BackgroundColor(
            normal=Colors.PRIMARY.withAlpha(0.15),
            hover=Colors.PRIMARY.withAlpha(0.25),
        )
        self.SUCCESS = BackgroundColor(
            normal=Colors.SUCCESS.withAlpha(0.15),
            hover=Colors.SUCCESS.withAlpha(0.25),
        )
        self.DANGER = BackgroundColor(
            normal=Colors.DANGER.withAlpha(0.15),
            hover=Colors.DANGER.withAlpha(0.25),
        )
        self.WARNING = BackgroundColor(
            normal=Colors.WARNING.withAlpha(0.15),
            hover=Colors.WARNING.withAlpha(0.25),
        )
        self.DISABLED = BackgroundColor(
            normal=Colors.DISABLED.withAlpha(0.15),
            hover=Colors.DISABLED.withAlpha(0.25),
        )
        self.HIDDEN_PRIMARY = BackgroundColor(
            normal=Colors.TRANSPARENT,
            hover=Colors.PRIMARY.withAlpha(0.15),
        )
        self.HIDDEN_SUCCESS = BackgroundColor(
            normal=Colors.TRANSPARENT,
            hover=Colors.SUCCESS.withAlpha(0.15),
        )
        self.HIDDEN_DANGER = BackgroundColor(
            normal=Colors.TRANSPARENT,
            hover=Colors.DANGER.withAlpha(0.15),
        )
        self.HIDDEN_WARNING = BackgroundColor(
            normal=Colors.TRANSPARENT,
            hover=Colors.WARNING.withAlpha(0.15),
        )
