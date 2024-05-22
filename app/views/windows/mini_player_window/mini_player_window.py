import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QWindow
from PyQt5.QtWinExtras import QWinThumbnailToolBar, QWinThumbnailToolButton

from app.common.others import appCenter, musicPlayer
from app.common.statics.qt import Icons
from app.common.statics.styles import Colors
from app.components.base import Component
from app.components.events import VisibleObserver, SignalConnector
from app.components.sliders import VerticalSlider
from app.components.windows.windows import TitleBarWindow
from app.views.windows.mini_player_window.current_song_info import CurrentSongInfo
from app.views.windows.mini_player_window.music_player_bar import MusicPlayerBar


class MiniPlayerWindow(TitleBarWindow, Component):

    def __init__(self, mainWindow: QWindow) -> None:
        self.__mainWindow = mainWindow
        super().__init__()
        super()._initComponent()

        self.setFixedWidth(720)
        self.setFixedHeight(540)
        self._volumeSlider.setValue(musicPlayer.getVolume())

        if musicPlayer.isPlaying():
            self.__onMusicPlaying()
        else:
            self.__onMusicPaused()

    def _createUI(self) -> None:
        self.setAttribute(Qt.WA_DeleteOnClose)
        self._inner.setClassName("rounded-12 bg-white dark:bg-dark")

        self._songInfo = CurrentSongInfo()
        self._songInfo.setContentsMargins(16, 32, 16, 16)

        self._musicPlayerBar = MusicPlayerBar()
        self._musicPlayerBar.setClassName("bg-none border-t border-gray-20 rounded-none")
        self._musicPlayerBar.setContentsMargins(16, 24, 16, 8)

        self.addWidget(self._songInfo, stretch=1)
        self.addWidget(self._musicPlayerBar, alignment=Qt.AlignBottom)

        self._volumeSlider = VerticalSlider(self._inner)
        self._volumeSlider.setFixedSize(40, 200)
        self._volumeSlider.setPageStep(0)
        self._volumeSlider.setMaximum(100)
        self._volumeSlider.setProperty("value", 0)
        self._volumeSlider.setSliderPosition(100)
        self._volumeSlider.setClassName(
            "rounded-8 bg-gray-[w8] track/inactive:bg-primary track/active:bg-gray",
            "dark:bg-gray-[b50] dark:handle/bg-white dark:track/inactive:bg-white dark:track/active:bg-gray"
        )
        self._volumeSlider.hide()
        observer = VisibleObserver(self._volumeSlider)
        observer.visible.connect(lambda: self.__moveVolumeSlider())

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

        self._signalConnector = SignalConnector(self)

    def translateUI(self) -> None:
        super().translateUI()
        self._maximizeBtn.setToolTip(self.translate("TITLE_BAR.EXIT_MINI_PLAYER_BTN"))

        playTooltip = "MUSIC_PLAYER.TOOLTIP_PAUSE_BTN" if musicPlayer.isPlaying() else "MUSIC_PLAYER.TOOLTIP_PLAY_BTN"

        self._toolbarPrevBtn.setToolTip(self.translate("MUSIC_PLAYER.TOOLTIP_PREV_BTN"))
        self._toolbarPlayBtn.setToolTip(self.translate(playTooltip))
        self._toolbarNextBtn.setToolTip(self.translate("MUSIC_PLAYER.TOOLTIP_NEXT_BTN"))

    def _connectSignalSlots(self) -> None:
        self._closeBtn.clicked.connect(lambda: appCenter.exited.emit())
        self._closeBtn.clicked.connect(lambda: sys.exit())

        self._maximizeBtn.clicked.connect(lambda: self.showMainWindow())
        self._minimizeBtn.clicked.connect(lambda: self.showMinimized())

        self._volumeSlider.valueChanged.connect(lambda: musicPlayer.setVolume(self._volumeSlider.value()))
        self._musicPlayerBar.volumeBtn.clicked.connect(lambda: self.__showVolumeSlider())

        self._toolbarPrevBtn.clicked.connect(lambda: musicPlayer.playPreviousSong())
        self._toolbarPlayBtn.clicked.connect(lambda: musicPlayer.pause() if musicPlayer.isPlaying() else musicPlayer.play())
        self._toolbarNextBtn.clicked.connect(lambda: musicPlayer.playNextSong())

        self._signalConnector.connect(musicPlayer.played, lambda: self.__onMusicPlaying())
        self._signalConnector.connect(musicPlayer.paused, lambda: self.__onMusicPlaying())
        self._signalConnector.connect(musicPlayer.volumeChanged, lambda volume: self._volumeSlider.setValue(volume))

    def __onMusicPlaying(self) -> None:
        self._toolbarPlayBtn.setIcon(Icons.pause.withColor(Colors.primary))
        self._toolbarPlayBtn.setToolTip(self.translate("MUSIC_PLAYER.TOOLTIP_PAUSE_BTN"))

    def __onMusicPaused(self) -> None:
        self._toolbarPlayBtn.setIcon(Icons.play.withColor(Colors.primary))
        self._toolbarPlayBtn.setToolTip(self.translate("MUSIC_PLAYER.TOOLTIP_PLAY_BTN"))

    def applyLightMode(self) -> None:
        super().applyLightMode()
        self.applyThemeToChildren()

    def applyDarkMode(self) -> None:
        super().applyDarkMode()
        self.applyThemeToChildren()

    def show(self) -> None:
        super().show()

        self.translateUI()
        children = self.findChildren(Component)
        for child in children:
            child.translateUI()

        self.applyTheme()
        self.moveToCenter()
        self._toolbar.setWindow(self.windowHandle())

    def close(self) -> bool:
        self._songInfo.deleteLater()
        self._musicPlayerBar.deleteLater()
        self._toolbar.deleteLater()
        return super().close()

    def showMainWindow(self) -> None:
        self.__mainWindow.show()
        self.close()

    def __showVolumeSlider(self) -> None:
        self._volumeSlider.setVisible(not self._volumeSlider.isVisible())

    def __moveVolumeSlider(self) -> None:
        volumeSliderPos = self._volumeSlider.mapToGlobal(self._inner.pos())
        volumeBtnPos = self._musicPlayerBar.volumeBtn.mapToGlobal(self._inner.pos())
        distance = volumeBtnPos - volumeSliderPos
        x = distance.x() + (self._musicPlayerBar.volumeBtn.width() - self._volumeSlider.width()) // 2
        y = distance.y() - self._volumeSlider.height() - 8
        self._volumeSlider.move(x, y)
