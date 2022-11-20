from modules.models.view.AppIcon import AppIcon
from modules.models.view.Background import Background
from modules.statics.view.Material import Backgrounds


class IconButtonStyle:
    light_mode_icon: AppIcon
    light_mode_background: Background
    dark_mode_icon: AppIcon
    dark_mode_background: Background

    def __init__(
        self,
        light_mode_icon: AppIcon,
        light_mode_background: Background = Backgrounds.TRANSPARENT,
        dark_mode_icon: AppIcon = None,
        dark_mode_background: Background = None
    ):
        self.light_mode_icon = light_mode_icon
        self.light_mode_background = light_mode_background

        self.dark_mode_icon = dark_mode_icon or light_mode_icon
        self.dark_mode_background = dark_mode_background or light_mode_background
