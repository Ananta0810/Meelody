from .slider.horizontal_slider import HorizontalSlider
from .slider.slider import Slider


class SliderFactory:
    def get(self, type: str) -> Slider:
        return HorizontalSlider()
