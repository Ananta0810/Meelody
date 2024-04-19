from app.components.base import Component
from app.components.windows import FramelessWindow
from app.views.player_bar import MusicPlayerBar


class MainWindow(FramelessWindow, Component):

    def __init__(self, width: int = 1280, height: int = 720):
        super().__init__()
        self.setFixedWidth(width)
        self.setFixedHeight(height)

        self._createUI()
        self.installEventFilter(self)

    def _createUI(self) -> None:
        self._musicPlayerBar = MusicPlayerBar()
        self._musicPlayerBar.setFixedHeight(96)
        self._musicPlayerBar.setObjectName("musicPlayer")
        self.addWidget(self._musicPlayerBar)
        pass

    def _connectSignalSlots(self) -> None:
        pass

    def _assignShortcuts(self) -> None:
        pass

    def applyDarkMode(self) -> None:
        pass

    def applyLightMode(self) -> None:
        pass
