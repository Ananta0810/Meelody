from typing import Optional

from PyQt5.QtGui import QShowEvent, QWheelEvent
from PyQt5.QtWidgets import QWidget

from app.components.base import Component
from app.components.widgets import Body


class HomeBody(Body, Component):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        super()._initComponent()
        self.setClassName("bg-none border-none")

    def _createUI(self) -> None:
        pass

    def wheelEvent(self, a0: QWheelEvent) -> None:
        # carouselY = self.__playlist_carousel.rect().y()
        # if carouselY <= a0.y() <= carouselY + self.__playlist_carousel.height():
        #     return
        return super().wheelEvent(a0)

    def setContentsMargins(self, left: int, top: int, right: int, bottom: int) -> None:
        self._inner.setContentsMargins(0, top, 0, bottom)
        # self._playlist_carousel.setContentsMargins(left, 0, right, 0)
        # self._current_playlist.setContentsMargins(left, 0, right, 0)

    def showEvent(self, event: QShowEvent) -> None:
        # self._current_playlist.setFixedHeight(self.height())
        # self._playlist_carousel.setFixedHeight(320)
        return super().showEvent(event)
