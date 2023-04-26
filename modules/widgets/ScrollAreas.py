from typing import Optional

from PyQt5.QtCore import pyqtSignal, QVariantAnimation, QEasingCurve
from PyQt5.QtGui import QWheelEvent
from PyQt5.QtWidgets import QScrollArea, QWidget

from modules.helpers.types.Decorators import override
from modules.helpers.types.Numbers import Numbers
from modules.models.view.Background import Background
from modules.models.view.builder.BackgroundThemeBuilder import BackgroundThemeBuilder
from modules.statics.view.Material import Backgrounds


class SmoothVerticalScrollArea(QScrollArea):
    scrolled = pyqtSignal()

    __itemHeight: int
    __animation: QVariantAnimation

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent=parent)
        self.__itemHeight = 0
        self.__animation = QVariantAnimation(self, valueChanged=self.__smooth_scroll, duration=1000)
        self.__animation.setEasingCurve(QEasingCurve.OutCubic)

    @override
    def wheelEvent(self, event: QWheelEvent) -> None:
        self.__animation.stop()
        return super().wheelEvent(event)

    def set_item_height(self, height: int) -> None:
        self.__itemHeight = height

    def set_animation_duration(self, duration: int) -> None:
        self.__animation.setDuration(duration)

    def set_animation_easing_curve(self, easing_curve: QEasingCurve) -> None:
        self.__animation.setEasingCurve(easing_curve)

    def _scroll_to_item_at(self, index: int) -> None:
        maxValue: int = self.verticalScrollBar().maximum()
        endValue: int = Numbers.clamp_int(index * self.__itemHeight, 0, maxValue)
        self.__animation.stop()
        self.__animation.setStartValue(self.verticalScrollBar().value())
        self.__animation.setEndValue(endValue)
        self.__animation.start()

    def __smooth_scroll(self, value: int) -> None:
        self.verticalScrollBar().setValue(value)

    @staticmethod
    def build_style(
        length: int = 4,
        background: Background = Backgrounds.TRANSPARENT
    ) -> str:
        element_type: str = "vertical"
        return "\n".join(
            [
                BackgroundThemeBuilder.build(element=f"QScrollBar::handle:{element_type}", element_size=length, background=background),
                f"QScrollBar:{element_type}{{border:none;background-color:transparent;width:{length}px}}",
                f"QScrollBar::sub-line:{element_type}{{border:none}}",
                f"QScrollBar::add-line:{element_type}{{border:none}}",
                f"QScrollBar::add-page:{element_type},QScrollBar::sub-page:{element_type}{{background-color:none}}",
                f"QScrollBar::up-arrow:{element_type},QScrollBar::down-arrow:{element_type}{{background-color:none}}",
            ]
        )

