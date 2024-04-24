from typing import Optional

from PyQt5.QtGui import QShowEvent
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea

from app.components.base import Component
from app.views.home.current_playlist import CurrentPlaylist


class HomeBody(QScrollArea, Component):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        super()._initComponent()
        self.setClassName("bg-none border-none")

    def _createUI(self) -> None:
        self._inner = QWidget()
        self.setWidget(self._inner)

        self._mainLayout = QVBoxLayout(self._inner)
        self._mainLayout.setContentsMargins(0, 0, 0, 0)
        self._mainLayout.setSpacing(50)

        self._currentPlaylist = CurrentPlaylist()
        self._mainLayout.addWidget(self._currentPlaylist)

    def setContentsMargins(self, left: int, top: int, right: int, bottom: int) -> None:
        self._inner.setContentsMargins(0, top, 0, bottom)
        self._currentPlaylist.setContentsMargins(left, 0, right, 0)

    def showEvent(self, event: QShowEvent) -> None:
        self._currentPlaylist.setFixedHeight(320)
        return super().showEvent(event)
