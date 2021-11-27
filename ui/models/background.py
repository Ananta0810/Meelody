from .background_color import BackgroundColor
from .border import Border


class Background:
    def __init__(
        self, color: BackgroundColor, border: Border = None, roundness: float = 0
    ):
        self.color = color
        self.border = border
        self.roundness = roundness
