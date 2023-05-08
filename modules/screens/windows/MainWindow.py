from typing import Callable

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QMenu, QAction, QSystemTrayIcon
from PyQt5.QtWinExtras import QWinThumbnailToolBar, QWinThumbnailToolButton

from modules.helpers.types.Decorators import override, connector
from modules.models.view.Background import Background
from modules.screens.AbstractScreen import BaseView
from modules.screens.body.HomeBodyView import HomeBodyView
from modules.screens.music_bar.MusicPlayerControl import MusicPlayerControl
from modules.statics.view.Material import ColorBoxes, Icons, Colors
from modules.widgets.Windows import CloseableWindow


class MainWindow(CloseableWindow, BaseView):
    _body: HomeBodyView
    _music_player: MusicPlayerControl
    post_show: pyqtSignal = pyqtSignal()

    def __init__(self, width: int = 1280, height: int = 720):
        super().__init__()
        self.__is_first_load = True

        self.setFixedWidth(width)
        self.setFixedHeight(height)
        self.__init_ui()
        self.__tray.setVisible(False)

        self.installEventFilter(self)

    def __init_ui(self) -> None:
        self._body = HomeBodyView()
        self._body.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._body.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._body.setWidgetResizable(True)
        self._body.setContentsMargins(72, 20, 50, 0)

        self._music_player = MusicPlayerControl()
        self._music_player.setFixedHeight(96)
        self._music_player.setObjectName("musicPlayer")

        self.addWidget(self._body)
        self.addWidget(self._music_player, alignment=Qt.AlignBottom)

        self.__tray = QSystemTrayIcon()
        self.__tray.setIcon(Icons.LOGO)
        self.__tray.setToolTip("Meelody")

        self.__tray_menu = QMenu()
        self.__tray_menu.setStyleSheet(
            """
                QMenu {
                    background-color: rgb(250, 250, 250);
                    border-color: rgb(225, 225, 225);
                    border-radius: 8px
                }
                QMenu::item {
                    border: none;
                    background-color: rgb(250,250,250);
                    min-width: 128px;
                    padding: 8 32 8 32;
                }
                QMenu::item:selected {
                    background-color: rgb(240, 240, 240);
                }
            """
        )

        show_action = QAction("Show", self)
        show_action.triggered.connect(self.show)
        self.__tray_menu.addAction(show_action)

        self.__play_action_btn = QAction(self)
        self.__play_action_btn.triggered.connect(lambda: self.__onclick_pause())
        self.__tray_menu.addAction(self.__play_action_btn)

        prev_action = QAction("Previous song", self)
        prev_action.triggered.connect(lambda: self.__onclick_prev_fn())
        self.__tray_menu.addAction(prev_action)

        next_action = QAction("Next song", self)
        next_action.triggered.connect(lambda: self.__onclick_next_fn())
        self.__tray_menu.addAction(next_action)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(lambda: self._exit())
        self.__tray_menu.addAction(exit_action)

        self.__tray.setContextMenu(self.__tray_menu)

        self.__toolbar = QWinThumbnailToolBar(self)

        # Prev, Play/Pause, Next
        self.__toolbar_prev_btn = QWinThumbnailToolButton(self.__toolbar)
        self.__toolbar_prev_btn.setToolTip('Previous')
        self.__toolbar_prev_btn.setIcon(Icons.PREVIOUS.with_color(Colors.PRIMARY))
        self.__toolbar_prev_btn.clicked.connect(lambda: self.__onclick_prev_fn())
        self.__toolbar.addButton(self.__toolbar_prev_btn)

        self.__toolbar_play_btn = QWinThumbnailToolButton(self.__toolbar)
        self.__toolbar_play_btn.setToolTip('Play')
        self.__toolbar_play_btn.setProperty('status', 0)
        self.__toolbar_play_btn.setIcon(Icons.PLAY.with_color(Colors.PRIMARY))
        self.__toolbar_play_btn.clicked.connect(lambda: self.__onclick_pause())
        self.__toolbar.addButton(self.__toolbar_play_btn)

        self.__toolbar_next_btn = QWinThumbnailToolButton(self.__toolbar)
        self.__toolbar_next_btn.setToolTip('Next')
        self.__toolbar_next_btn.setIcon(Icons.NEXT.with_color(Colors.PRIMARY))
        self.__toolbar_next_btn.clicked.connect(lambda: self.__onclick_next_fn())
        self.__toolbar.addButton(self.__toolbar_next_btn)

    def show(self) -> None:
        self.__tray.hide()
        super().show()

    def hide(self) -> None:
        self.__tray.show()
        super().hide()

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        super().showEvent(a0)
        if not self.__toolbar.window():
            self.__toolbar.setWindow(self.windowHandle())
        if self.__is_first_load:
            self.post_show.emit()
            self.__is_first_load = False
            self.moveToCenter()

    @override
    def apply_light_mode(self) -> None:
        super().apply_light_mode()
        self.setStyleSheet(Background(border_radius=32, color=ColorBoxes.WHITE).to_stylesheet())
        self._body.apply_light_mode()
        self._music_player.setStyleSheet("QWidget#musicPlayer{border-top: 1px solid #eaeaea};border-radius:0px")
        self._music_player.apply_light_mode()

    @override
    def apply_dark_mode(self) -> None:
        super().apply_dark_mode()
        self.setStyleSheet(Background(border_radius=32, color=ColorBoxes.BLACK).to_stylesheet())
        self._body.apply_dark_mode()
        self._music_player.setStyleSheet("QWidget#musicPlayer{border-top: 1px solid #202020};border-radius:0px")
        self._music_player.apply_dark_mode()

    def _set_default_playlist_cover(self, cover: bytes):
        self._body.set_default_playlist_cover(cover)

    def set_is_playing(self, is_playing: bool) -> None:
        self.__is_playing = is_playing
        self.__set_play_btn_text(is_playing)

    def __onclick_pause(self) -> None:
        if self.__is_playing:
            self.__is_playing = False
            self.__onclick_pause_fn()
        else:
            self.__is_playing = True
            self.__onclick_play_fn()
        self.__set_play_btn_text(self.__is_playing)

    def __set_play_btn_text(self, is_playing: bool) -> None:
        text = "Pause" if is_playing else "Play"
        self.__play_action_btn.setText(text)
        self.__toolbar_play_btn.setToolTip(text)
        self.__toolbar_play_btn.setIcon(
            Icons.PAUSE.with_color(Colors.PRIMARY)
            if is_playing
            else Icons.PLAY.with_color(Colors.PRIMARY)
        )

    @connector
    def __onclick_play(self) -> None:
        self.__onclick_play_fn()

    @connector
    def set_onclick_play_on_tray(self, fn: Callable[[], None]) -> None:
        self.__onclick_play_fn = fn

    @connector
    def set_onclick_pause_on_tray(self, fn: Callable[[], None]) -> None:
        self.__onclick_pause_fn = fn

    @connector
    def set_onclick_prev_on_tray(self, fn: Callable[[], None]) -> None:
        self.__onclick_prev_fn = fn

    @connector
    def set_onclick_next_on_tray(self, fn: Callable[[], None]) -> None:
        self.__onclick_next_fn = fn
