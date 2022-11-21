from modules.models.view.Background import Background
from modules.models.view.ColorBox import ColorBox
from modules.statics.view.Material import Backgrounds, ColorBoxes


class SliderStyle:
    handler_color: ColorBox
    track_active_color: ColorBox
    track_inactive_color: ColorBox
    background: Background

    def __init__(
        self,
        handler_color: ColorBox = ColorBoxes.BLACK,
        track_active_color: ColorBox = ColorBoxes.BLACK,
        track_inactive_color: ColorBox = ColorBoxes.GRAY_50,
        background: Background = Backgrounds.TRANSPARENT
    ):
        self.handler_color = handler_color
        self.track_active_color = track_active_color
        self.track_inactive_color = track_inactive_color
        self.background = background
