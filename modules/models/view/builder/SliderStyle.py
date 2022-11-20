from modules.models.view.Background import Background
from modules.models.view.ColorBox import ColorBox
from modules.statics.view.Material import Backgrounds, ColorBoxes


class SliderStyle:
    handler_color: ColorBox
    line_color: ColorBox
    background: Background

    def __init__(
        self,
        handler_color: ColorBox = ColorBoxes.BLACK,
        line_color: ColorBox = ColorBoxes.BLACK,
        background: Background = Backgrounds.TRANSPARENT
    ):
        self.handler_color = handler_color
        self.line_color = line_color
        self.background = background
