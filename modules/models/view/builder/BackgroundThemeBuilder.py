from modules.helpers.types import Strings
from modules.models.view.Background import Background
from modules.models.view.ColorBox import ColorBox
from modules.statics.view.Material import Backgrounds, ColorBoxes


class BackgroundThemeBuilder:
    BUTTON = "QPushButton"
    LABEL = "QLabel,QLineEdit,QPushButton"
    SLIDER = "QSlider"

    @staticmethod
    def build(
        element: str,
        element_size: float,
        background: Background = Backgrounds.TRANSPARENT,
        text_color: ColorBox = ColorBoxes.TRANSPARENT,
        padding: int = 0,
    ) -> str:
        normal_content: str = BackgroundThemeBuilder.__build_content(padding, element_size, text_color, background)
        hover_content: str = BackgroundThemeBuilder.__build_content(padding, element_size, text_color, background, is_hover=True)
        return Strings.unindent(
            f"""
            {element} {{{normal_content}}}
            {element}:hover, {element}[hovered=true] {{{hover_content}}}"""
        )

    @staticmethod
    def __build_content(
        padding: int,
        element_size: float,
        text_color: ColorBox = ColorBoxes.TRANSPARENT,
        background: Background = Backgrounds.TRANSPARENT,
        is_hover: bool = False
    ) -> str:
        text_color = text_color.to_stylesheet(is_hover)
        background_style = background.to_stylesheet(border_radius_size=element_size, active_color=is_hover, active_border=is_hover).removeprefix("\n")
        return \
            f"""
            color:{text_color};
            padding:{padding}px;
            {background_style}"""
