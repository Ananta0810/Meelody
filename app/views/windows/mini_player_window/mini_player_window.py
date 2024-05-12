from PyQt5.QtCore import Qt
from PyQt5.QtGui import QWindow
from PyQt5.QtWinExtras import QWinThumbnailToolBar, QWinThumbnailToolButton

from app.common.others import appCenter, musicPlayer, translator
from app.common.statics.qt import Icons
from app.common.statics.styles import Colors
from app.components.base import Component
from app.components.windows.windows import TitleBarWindow
from app.views.windows.mini_player_window.music_player_bar import MusicPlayerBar


class MiniPlayerWindow(TitleBarWindow, Component):

    def __init__(self, mainWindow: QWindow) -> None:
        self.__mainWindow = mainWindow
        super().__init__()
        super()._initComponent()

        self.setFixedWidth(720)
        self.setFixedHeight(540)

    def _createUI(self) -> None:
        self._inner.setClassName("rounded-24 bg-white dark:bg-dark")

        self._musicPlayerBar = MusicPlayerBar()
        self._musicPlayerBar.setClassName("bg-none border-t border-gray-20 rounded-none")
        self._musicPlayerBar.setContentsMargins(16, 24, 16, 8)

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

    def _translateUI(self) -> None:
        playTooltip = "MUSIC_PLAYER.TOOLTIP_PAUSE_BTN" if musicPlayer.isPlaying() else "MUSIC_PLAYER.TOOLTIP_PLAY_BTN"

        self._toolbarPrevBtn.setToolTip(translator.translate("MUSIC_PLAYER.TOOLTIP_PREV_BTN"))
        self._toolbarPlayBtn.setToolTip(translator.translate(playTooltip))
        self._toolbarNextBtn.setToolTip(translator.translate("MUSIC_PLAYER.TOOLTIP_NEXT_BTN"))

    def _connectSignalSlots(self) -> None:
        self._closeBtn.clicked.connect(lambda: appCenter.exited.emit())
        self._maximizeBtn.clicked.connect(lambda: self.showMainWindow())
        self._minimizeBtn.clicked.connect(lambda: self.showMinimized())

        self._toolbarPrevBtn.clicked.connect(lambda: musicPlayer.playPreviousSong())
        self._toolbarPlayBtn.clicked.connect(lambda: musicPlayer.pause() if musicPlayer.isPlaying() else musicPlayer.play())
        self._toolbarNextBtn.clicked.connect(lambda: musicPlayer.playNextSong())

        musicPlayer.played.connect(lambda: self._toolbarPlayBtn.setToolTip(translator.translate("MUSIC_PLAYER.TOOLTIP_PAUSE_BTN")))
        musicPlayer.played.connect(lambda: self._toolbarPlayBtn.setIcon(Icons.pause.withColor(Colors.primary)))

        musicPlayer.paused.connect(lambda: self._toolbarPlayBtn.setToolTip(translator.translate("MUSIC_PLAYER.TOOLTIP_PLAY_BTN")))
        musicPlayer.paused.connect(lambda: self._toolbarPlayBtn.setIcon(Icons.play.withColor(Colors.primary)))

    def applyLightMode(self) -> None:
        super().applyLightMode()
        self.applyThemeToChildren()

    def applyDarkMode(self) -> None:
        super().applyDarkMode()
        self.applyThemeToChildren()

    def show(self) -> None:
        super().show()
        self.applyTheme()
        self.moveToCenter()
        self._toolbar.setWindow(self.windowHandle())

    def showMainWindow(self) -> None:
        self.__mainWindow.show()
        self.close()
