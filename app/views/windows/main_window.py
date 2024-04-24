from PyQt5.QtCore import Qt

from app.components.base import Component
from app.components.windows import FramelessWindow
from app.views.home import HomeBody
from app.views.player_bar import MusicPlayerBar


class MainWindow(FramelessWindow, Component):

    def __init__(self, width: int = 1280, height: int = 720) -> None:
        super().__init__()
        super()._initComponent()

        self.setFixedWidth(width)
        self.setFixedHeight(height)
        self.moveToCenter()
        self.setClassName("rounded-32 bg-white")

    def _createUI(self) -> None:
        self._body = HomeBody()
        self._body.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._body.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._body.setWidgetResizable(True)
        self._body.setContentsMargins(72, 20, 50, 0)

        self._musicPlayerBar = MusicPlayerBar()
        self._musicPlayerBar.setFixedHeight(96)
        self._musicPlayerBar.setObjectName("musicPlayer")

        self.addWidget(self._body)
        self.addWidget(self._musicPlayerBar, alignment=Qt.AlignBottom)

    def applyLightMode(self) -> None:
        super().applyLightMode()
        self._musicPlayerBar.setStyleSheet("QWidget#musicPlayer{border-top: 1px solid #eaeaea};border-radius:0px")

    def applyDarkMode(self) -> None:
        super().applyDarkMode()
        self._musicPlayerBar.setStyleSheet("QWidget#musicPlayer{border-top: 1px solid #202020};border-radius:0px")
