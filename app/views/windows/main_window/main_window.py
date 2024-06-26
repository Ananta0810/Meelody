import sys

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QShowEvent
from PyQt5.QtWinExtras import QWinThumbnailToolBar, QWinThumbnailToolButton

from app.common.others import appCenter, musicPlayer
from app.common.statics.qt import Icons
from app.common.statics.styles import Colors
from app.components.base import Component
from app.components.windows.windows import TitleBarWindow
from app.utils.base import Strings
from app.views.windows.main_window.home import HomeBody
from app.views.windows.main_window.player_bar import MusicPlayerBar
from app.views.windows.mini_player_window.mini_player_window import MiniPlayerWindow


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
        self._toolbarPrevBtn.setIcon(Icons.previous.withColor(Colors.primary))

        self._toolbarPlayBtn = QWinThumbnailToolButton()
        self._toolbarPlayBtn.setProperty('status', 0)
        self._toolbarPlayBtn.setIcon(Icons.play.withColor(Colors.primary))

        self._toolbarNextBtn = QWinThumbnailToolButton()
        self._toolbarNextBtn.setIcon(Icons.next.withColor(Colors.primary))

        self._toolbar = QWinThumbnailToolBar()
        self._toolbar.addButton(self._toolbarPrevBtn)
        self._toolbar.addButton(self._toolbarPlayBtn)
        self._toolbar.addButton(self._toolbarNextBtn)

    def translateUI(self) -> None:
        super().translateUI()
        self._maximizeBtn.setToolTip(self.translate("TITLE_BAR.MINI_PLAYER_BTN"))

        playTooltip = "MUSIC_PLAYER.TOOLTIP_PAUSE_BTN" if musicPlayer.isPlaying() else "MUSIC_PLAYER.TOOLTIP_PLAY_BTN"

        self._toolbarPrevBtn.setToolTip(self.translate("MUSIC_PLAYER.TOOLTIP_PREV_BTN"))
        self._toolbarPlayBtn.setToolTip(self.translate(playTooltip))
        self._toolbarNextBtn.setToolTip(self.translate("MUSIC_PLAYER.TOOLTIP_NEXT_BTN"))

    def _connectSignalSlots(self) -> None:
        self._minimizeBtn.clicked.connect(lambda: self.showMinimized())
        self._maximizeBtn.clicked.connect(lambda: self.showMiniPlayerWindow())
        self._closeBtn.clicked.connect(lambda: appCenter.exited.emit())
        self._closeBtn.clicked.connect(lambda: sys.exit())

        self._toolbarPrevBtn.clicked.connect(lambda: musicPlayer.playPreviousSong())
        self._toolbarPlayBtn.clicked.connect(lambda: musicPlayer.pause() if musicPlayer.isPlaying() else musicPlayer.play())
        self._toolbarNextBtn.clicked.connect(lambda: musicPlayer.playNextSong())

        musicPlayer.played.connect(lambda: self._toolbarPlayBtn.setToolTip(self.translate("MUSIC_PLAYER.TOOLTIP_PAUSE_BTN")))
        musicPlayer.played.connect(lambda: self._toolbarPlayBtn.setIcon(Icons.pause.withColor(Colors.primary)))

        musicPlayer.paused.connect(lambda: self._toolbarPlayBtn.setToolTip(self.translate("MUSIC_PLAYER.TOOLTIP_PLAY_BTN")))
        musicPlayer.paused.connect(lambda: self._toolbarPlayBtn.setIcon(Icons.play.withColor(Colors.primary)))

        appCenter.library.getSongs().updated.connect(lambda: self._disableMinimizePlayerIfNoSongInLibrary())

    def show(self) -> None:
        super().show()
        self.moveToCenter()
        self._toolbar.setWindow(self.windowHandle())
        self._disableMinimizePlayerIfNoSongInLibrary()

    def showEvent(self, a0: QShowEvent) -> None:
        super().showEvent(a0)
        if not appCenter.isLoaded:
            timer = QTimer(self)
            timer.setSingleShot(True)
            timer.timeout.connect(lambda: appCenter.loaded.emit())
            timer.start(10)

    def showMiniPlayerWindow(self) -> None:
        if appCenter.library.getSongs().hasAnySong():
            self.hide()
            window = MiniPlayerWindow(self)
            window.show()

    def _disableMinimizePlayerIfNoSongInLibrary(self) -> None:
        self._maximizeBtn.setDisabled(not appCenter.library.getSongs().hasAnySong())
