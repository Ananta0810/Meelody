from typing import Optional

from PyQt5.QtCore import pyqtSignal, QVariantAnimation, QEasingCurve
from PyQt5.QtGui import QWheelEvent
from PyQt5.QtWidgets import QScrollArea, QWidget

from app.components.base import Component
from app.helpers.base import Numbers, Strings
from app.helpers.stylesheets.translators import ClassNameTranslator
from app.helpers.stylesheets.translators.classname_translator import ClassNameTheme


class SmoothVerticalScrollArea(QScrollArea, Component):
    scrolled = pyqtSignal()

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent=parent)
        self.__scrollBarWidth = 4
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

    def setClassName(self, *classNames: str) -> None:
        light, dark = ClassNameTranslator.translateElements(Strings.join(" ", classNames), self)

        self._lightModeStyle = self.__buildStyle(light)
        self._darkModeStyle = self.__buildStyle(dark)

    def __buildStyle(self, theme: ClassNameTheme) -> str:
        direction: str = "vertical"
        return f"""
                    QScrollArea {{ background: transparent; border: none; }}
                    QScrollArea > QWidget > QWidget {{ background: transparent; border: none; }}
                    QScrollArea > QWidget > QScrollBar {{ background: palette(base); border: none; }}
                    QScrollBar::handle:{direction} {{{theme.getElement("scroll").state("none").toProps() or ""}}}
                    QScrollBar::handle:{direction}:hover {{{theme.getElement("scroll").state("hover").toProps() or ""}}}
                    QScrollBar:{direction}{{border:none;background-color:transparent;width:{self.__scrollBarWidth}px}}
                    QScrollBar::sub-line:{direction}{{border:none}}
                    QScrollBar::add-line:{direction}{{border:none}}
                    QScrollBar::add-page:{direction},QScrollBar::sub-page:{direction}{{background-color:none}}
                    QScrollBar::up-arrow:{direction},QScrollBar::down-arrow:{direction}{{background-color:none}}
                """
