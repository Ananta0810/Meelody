from typing import Optional, Union

from PyQt5.QtCore import pyqtSignal, QVariantAnimation, QEasingCurve, Qt
from PyQt5.QtGui import QWheelEvent
from PyQt5.QtWidgets import QWidget

from app.components.scroll_areas.style_scroll_area import StyleScrollArea
from app.components.widgets import Box
from app.helpers.base import Numbers
from app.helpers.qt import Widgets


class SmoothVerticalScrollArea(StyleScrollArea):
    scrolled = pyqtSignal()

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent=parent)

        self.__widgets: list[QWidget] = []
        self.__visibleWidgetIndexes: set[int] = set()

        self.__animation = QVariantAnimation(self, valueChanged=self.__smoothScroll, duration=1000)
        self.__animation.setEasingCurve(QEasingCurve.OutCubic)

    def _createUI(self) -> None:
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        self._menu = QWidget()
        self._menu.setStyleSheet("background:transparent;border:none")
        self._menu.setContentsMargins(8, 0, 8, 8)

        self._mainLayout = Box(self._menu)
        self._mainLayout.setAlignment(Qt.AlignTop)

        self.setWidget(self._menu)

    def _connectSignalSlots(self) -> None:
        self.verticalScrollBar().valueChanged.connect(self.__updateVisibleItems)

    def setContentsMargins(self, left: int, top: int, right: int, bottom: int) -> None:
        self._menu.setContentsMargins(left, top, right, bottom)

    def widgets(self) -> list[QWidget]:
        return self.__widgets

    def addWidget(self, widget: QWidget, stretch: int = None, alignment: Union[Qt.Alignment, Qt.AlignmentFlag] = None) -> None:
        self._mainLayout.addWidget(widget, stretch, alignment)
        self.__widgets.append(widget)

    def removeWidget(self, widget: QWidget) -> None:
        self._mainLayout.removeWidget(widget)
        self.__widgets.remove(widget)

    def moveWidget(self, widget: QWidget, newIndex: int) -> None:
        self.__widgets.remove(widget)
        self.__widgets.insert(newIndex, widget)

        self._mainLayout.removeWidget(widget)
        self._mainLayout.insertWidget(newIndex, widget)

    def __updateVisibleItems(self):
        self.__visibleWidgetIndexes = {index for index, item in enumerate(self.__widgets) if Widgets.isInView(item)}

    def wheelEvent(self, event: QWheelEvent) -> None:
        self.__animation.stop()
        return super().wheelEvent(event)

    def setAnimationDuration(self, duration: int) -> None:
        self.__animation.setDuration(duration)

    def setAnimationEasingCurve(self, easing_curve: QEasingCurve) -> None:
        self.__animation.setEasingCurve(easing_curve)

    def getCurrentItemIndex(self):
        return min(self.__visibleWidgetIndexes)

    def scrollToItemAt(self, index: int) -> None:
        try:
            item = self.__widgets[index]
            itemPosition = item.mapToParent(self.pos()) - self.__widgets[0].mapToParent(self.pos())
            targetPosition: int = Numbers.clamp(itemPosition.y(), 0, self.verticalScrollBar().maximum())

            self.__animation.stop()
            self.__animation.setStartValue(self.verticalScrollBar().value())
            self.__animation.setEndValue(targetPosition)
            self.__animation.start()
        except IndexError:
            pass

    def __smoothScroll(self, value: int) -> None:
        self.verticalScrollBar().setValue(value)
