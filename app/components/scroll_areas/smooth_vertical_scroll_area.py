from typing import Optional

from PyQt5.QtCore import pyqtSignal, QVariantAnimation, QEasingCurve
from PyQt5.QtGui import QWheelEvent
from PyQt5.QtWidgets import QScrollArea, QWidget

from app.components.base import Component
from app.helpers.base import Numbers


class SmoothVerticalScrollArea(QScrollArea, Component):
    scrolled = pyqtSignal()

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent=parent)
        self.__itemHeight = 0
        self.__animation = QVariantAnimation(self, valueChanged=self.__smoothScroll, duration=1000)
        self.__animation.setEasingCurve(QEasingCurve.OutCubic)

    def wheelEvent(self, event: QWheelEvent) -> None:
        self.__animation.stop()
        return super().wheelEvent(event)

    def setItemHeight(self, height: int) -> None:
        self.__itemHeight = height

    def setAnimationDuration(self, duration: int) -> None:
        self.__animation.setDuration(duration)

    def setAnimationEasingCurve(self, easing_curve: QEasingCurve) -> None:
        self.__animation.setEasingCurve(easing_curve)

    def _scrollToItemAt(self, index: int) -> None:
        maxValue: int = self.verticalScrollBar().maximum()
        endValue: int = Numbers.clamp(index * self.__itemHeight, 0, maxValue)
        self.__animation.stop()
        self.__animation.setStartValue(self.verticalScrollBar().value())
        self.__animation.setEndValue(endValue)
        self.__animation.start()

    def getCurrentItemIndex(self):
        return self.verticalScrollBar().value() // self.__itemHeight

    def __smoothScroll(self, value: int) -> None:
        self.verticalScrollBar().setValue(value)

    # @staticmethod
    # def build_style(
    #     length: int = 4,
    #     background: Background = Backgrounds.TRANSPARENT
    # ) -> str:
    #     element_type: str = "vertical"
    #     return "\n".join(
    #         [
    #             """
    #                 QScrollArea { background: transparent; border: none; }
    #                 QScrollArea > QWidget > QWidget { background: transparent; border: none; }
    #                 QScrollArea > QWidget > QScrollBar { background: palette(base); border: none; }
    #             """,
    #             BackgroundThemeBuilder.build(element=f"QScrollBar::handle:{element_type}", element_size=length,
    #                                          background=background),
    #             f"QScrollBar:{element_type}{{border:none;background-color:transparent;width:{length}px}}",
    #             f"QScrollBar::sub-line:{element_type}{{border:none}}",
    #             f"QScrollBar::add-line:{element_type}{{border:none}}",
    #             f"QScrollBar::add-page:{element_type},QScrollBar::sub-page:{element_type}{{background-color:none}}",
    #             f"QScrollBar::up-arrow:{element_type},QScrollBar::down-arrow:{element_type}{{background-color:none}}",
    #         ]
    #     )
