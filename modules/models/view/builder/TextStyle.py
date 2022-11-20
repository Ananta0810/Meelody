from modules.models.view.Background import Background
from modules.models.view.ColorBox import ColorBox
from modules.statics.view.Material import Backgrounds, ColorBoxes


class TextStyle:
    text_color: ColorBox
    background: Background

    def __init__(self, text_color: ColorBox = ColorBoxes.BLACK, background: Background = Backgrounds.TRANSPARENT):
        self.text_color = text_color
        self.background = background
