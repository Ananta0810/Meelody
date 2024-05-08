from PyQt5.QtCore import Qt
from PyQt5.QtWinExtras import QWinThumbnailToolBar, QWinThumbnailToolButton

from app.common.others import appCenter, musicPlayer
from app.components.base import Component
from app.components.windows.windows import TitleBarWindow
from app.helpers.base import Strings
from app.helpers.stylesheets import Colors
from app.resource.qt import Icons
from app.views.home import HomeBody
from app.views.player_bar import MusicPlayerBar


class MainWindow(TitleBarWindow, Component):

    def __init__(self, width: int = 1280, height: int = 720) -> None:
        super().__init__()
        self.setObjectName(Strings.randomId())
        super()._initComponent()

        self.setFixedWidth(width)
        self.setFixedHeight(height)

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
        self._musicPlayerBar.setClassName("bg-none border-t border-gray-20 rounded-none")

        self.addWidget(self._body)
        self.addWidget(self._musicPlayerBar, alignment=Qt.AlignBottom)

        # Prev, Play/Pause, Next
        self._toolbarPrevBtn = QWinThumbnailToolButton()
        self._toolbarPrevBtn.setToolTip('Previous')
        self._toolbarPrevBtn.setIcon(Icons.PREVIOUS.withColor(Colors.PRIMARY))

        self._toolbarPlayBtn = QWinThumbnailToolButton()
        self._toolbarPlayBtn.setToolTip('Play')
        self._toolbarPlayBtn.setProperty('status', 0)
        self._toolbarPlayBtn.setIcon(Icons.PLAY.withColor(Colors.PRIMARY))

        self._toolbarNextBtn = QWinThumbnailToolButton()
        self._toolbarNextBtn.setToolTip('Next')
        self._toolbarNextBtn.setIcon(Icons.NEXT.withColor(Colors.PRIMARY))

        self._toolbar = QWinThumbnailToolBar()
        self._toolbar.addButton(self._toolbarPrevBtn)
        self._toolbar.addButton(self._toolbarPlayBtn)
        self._toolbar.addButton(self._toolbarNextBtn)

    def _connectSignalSlots(self) -> None:
        self._closeBtn.clicked.connect(lambda: appCenter.exited.emit())

        self._toolbarPrevBtn.clicked.connect(lambda: musicPlayer.playPreviousSong())
        self._toolbarPlayBtn.clicked.connect(lambda: musicPlayer.pause() if musicPlayer.isPlaying() else musicPlayer.play())
        self._toolbarNextBtn.clicked.connect(lambda: musicPlayer.playNextSong())

        musicPlayer.played.connect(lambda: self._toolbarPlayBtn.setToolTip("Pause"))
        musicPlayer.played.connect(lambda: self._toolbarPlayBtn.setIcon(Icons.PAUSE.withColor(Colors.PRIMARY)))

        musicPlayer.paused.connect(lambda: self._toolbarPlayBtn.setToolTip("Play"))
        musicPlayer.paused.connect(lambda: self._toolbarPlayBtn.setIcon(Icons.PLAY.withColor(Colors.PRIMARY)))

    def applyLightMode(self) -> None:
        super().applyLightMode()

    def applyDarkMode(self) -> None:
        super().applyDarkMode()

    def show(self) -> None:
        super().show()
        self.moveToCenter()
        self._toolbar.setWindow(self.windowHandle())
