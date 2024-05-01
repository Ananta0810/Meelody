from PyQt5.QtCore import Qt

from app.common.others import appCenter
from app.components.base import Component
from app.components.windows.windows import TitleBarWindow
from app.helpers.base import Strings
from app.views.home import HomeBody
from app.views.player_bar import MusicPlayerBar


class MainWindow(TitleBarWindow, Component):

    def __init__(self, width: int = 1280, height: int = 720) -> None:
        super().__init__()
        self.setObjectName(Strings.randomId())
        super()._initComponent()

        self.setFixedWidth(width)
        self.setFixedHeight(height)
        self.moveToCenter()

    def _createUI(self) -> None:
        self._inner.setClassName("rounded-24 bg-white dark:bg-dark")

        self._body = HomeBody()
        self._body.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._body.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._body.setWidgetResizable(True)
        self._body.setContentsMargins(64, 0, 50, 0)

        self._musicPlayerBar = MusicPlayerBar()
        self._musicPlayerBar.setFixedHeight(96)
        self._musicPlayerBar.setContentsMargins(16, 0, 16, 0)
        self._musicPlayerBar.setClassName("bg-none border-none border-t-gray-20 rounded-none")

        self.addWidget(self._body)
        self.addWidget(self._musicPlayerBar, alignment=Qt.AlignBottom)

    def _connectSignalSlots(self) -> None:
        self._closeBtn.clicked.connect(lambda: appCenter.exited.emit())

    def applyLightMode(self) -> None:
        super().applyLightMode()

    def applyDarkMode(self) -> None:
        super().applyDarkMode()
