from typing import Optional

from PyQt5.QtCore import pyqtSignal, QVariantAnimation, QEasingCurve
from PyQt5.QtGui import QWheelEvent
from PyQt5.QtWidgets import QScrollArea, QWidget

from modules.helpers.types.Numbers import Numbers
from modules.models.view.Background import Background
from modules.models.view.builder.BackgroundThemeBuilder import BackgroundThemeBuilder
from modules.statics.view.Material import Backgrounds


class SmoothVerticalScrollArea(QScrollArea):
    scrolled = pyqtSignal()

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent=parent)
        self._itemHeight = 0
        self._animation = QVariantAnimation(self, valueChanged=self.__smooth_scroll, duration=1000)
        self._animation.setEasingCurve(QEasingCurve.OutCubic)

    def wheelEvent(self, event: QWheelEvent) -> None:
        self._animation.stop()
        return super().wheelEvent(event)

    def set_item_height(self, height: int) -> None:
        self._itemHeight = height

    def set_animation_duration(self, duration: int) -> None:
        self._animation.setDuration(duration)

    def set_animation_easing_curve(self, easing_curve: QEasingCurve) -> None:
        self._animation.setEasingCurve(easing_curve)

    def scroll_to_item(self, item: int) -> None:
        maxValue: int = self.verticalScrollBar().maximum()
        endValue: int = Numbers.clamp_int(item * self._itemHeight, 0, maxValue)
        self._animation.stop()
        self._animation.setStartValue(self.verticalScrollBar().value())
        self._animation.setEndValue(endValue)
        self._animation.start()

    def __smooth_scroll(self, value: int) -> None:
        self.verticalScrollBar().setValue(value)

    @staticmethod
    def build_style(
        length: int = 4,
        type: str = "vertical",
        background: Background = Backgrounds.TRANSPARENT
    ) -> str:
        return "".join(
            [
                BackgroundThemeBuilder.build(element=f"QScrollBar::handle:{type}", element_size=length, background=background),
                f"QScrollBar:{type}{{border:none;background-color:transparent;width:{length}px}}",
                f"QScrollBar::sub-line:{type}{{border:none}}",
                f"QScrollBar::add-line:{type}{{border:none}}",
                f"QScrollBar::add-page:{type},QScrollBar::sub-page:{type}{{background-color:none}}",
                f"QScrollBar::up-arrow:{type},QScrollBar::down-arrow:{type}{{background-color:none}}",
            ]
        )

