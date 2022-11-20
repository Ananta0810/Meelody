from modules.models.view.builder.BackgroundThemeBuilder import BackgroundThemeBuilder
from modules.models.view.builder.SliderStyle import SliderStyle


class HorizontalSliderThemeBuilder:

    @staticmethod
    def build(
        style: SliderStyle,
        item_size: int,
        handle_size: int = 10,
        line_size: int = 2,
    ) -> str:
        line_radius = line_size // 2
        line_margin = (item_size - line_size) // 2
        handle_margin = (item_size - handle_size) // 2
        return (
            f"""
            {BackgroundThemeBuilder.build(BackgroundThemeBuilder.SLIDER, item_size, background=style.background)}
            QSlider::groove{{border:none}}
            QSlider::add-page {{
                 border:none;
                background:{style.line_color.to_stylesheet()};
                border-radius:{line_radius}px;
                margin:{line_margin}px {handle_margin}px {line_margin}px 0px
            }}
            QSlider::sub-page {{
                 border:none;
                background:{style.handler_color.to_stylesheet()};
                border-radius:{line_radius}px;
                margin:{line_margin}px 0px {line_margin}px {handle_margin + 1}px
            }}
            QSlider::handle {{
                border:none;
                background:{style.handler_color.to_stylesheet()};
                border-radius:{handle_size // 2}px;
                width:{handle_size}px;
                margin:{handle_margin}px {handle_margin + 1}px
            }}
            QSlider::handle:hover {{
                background:{style.handler_color.to_stylesheet(active=True)};
                width:{handle_size + 2}px;
                border-radius:{handle_size // 2 + 1}px;
                margin:{handle_margin - 1}px {handle_margin}px
            }}
            """
        )
