from typing import Optional, Callable, Union

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QKeyEvent, QResizeEvent
from PyQt5.QtWidgets import QWidget, QMenu, QAction, QSystemTrayIcon, QGraphicsDropShadowEffect
from PyQt5.QtWinExtras import QWinThumbnailToolBar, QWinThumbnailToolButton

from modules.helpers.types.Decorators import override, connector
from modules.models.view.Background import Background
from modules.screens.AbstractScreen import BaseView
from modules.screens.body.HomeBodyView import HomeBodyView
from modules.screens.music_bar.MusicPlayerControl import MusicPlayerControl
from modules.statics.view.Material import ColorBoxes, Icons, Colors
from modules.widgets import Dialogs
from modules.widgets.BaseDialogs import AlertDialog, ConfirmDialog, Dialog
from modules.widgets.DialogWindow import DialogWindow
from modules.widgets.Shortcut import Shortcut
from modules.widgets.Windows import FramelessWindow


class MainWindow(FramelessWindow, BaseView):
    _body: HomeBodyView
    _music_player: MusicPlayerControl
    post_show: pyqtSignal = pyqtSignal()

    def __init__(self, parent: Optional["QWidget"] = None, width: int = 1280, height: int = 720):
        super(MainWindow, self).__init__(parent)
        self.setFixedWidth(width)
        self.setFixedHeight(height)
        self.__init_ui()
        self._overlay.hide()
        self.__tray.setVisible(False)

        Dialogs.Dialogs.get_instance().set_window(self)
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

        self._overlay = WindowOverlay(self._inner)

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
        show_action.triggered.connect(lambda: self.__clicked_show_btn())
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
        exit_action.triggered.connect(lambda: self.__exit())
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

    @override
    def resizeEvent(self, event: QResizeEvent) -> None:
        self._overlay.resize(self.size())
        self._overlay.raise_()
        return super().resizeEvent(event)

    @override
    def keyPressEvent(self, event: QKeyEvent) -> None:
        shortcut = Shortcut.of(event.modifiers(), event.key())
        shortcut_map = self.get_shortcut_map()
        if shortcut in shortcut_map:
            fn = shortcut_map[shortcut]
            fn() if fn is not None else None

        return super().keyPressEvent(event)

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        super().showEvent(a0)
        if not self.__toolbar.window():
            self.__toolbar.setWindow(self.windowHandle())
        self.post_show.emit()

    @override
    def apply_light_mode(self) -> None:
        super().apply_light_mode()
        self.setStyleSheet(Background(border_radius=32, color=ColorBoxes.WHITE).to_stylesheet())
        self._body.apply_light_mode()
        self._music_player.setStyleSheet("QWidget#musicPlayer{border-top: 1px solid #eaeaea};border-radius:0px")
        self._music_player.apply_light_mode()
        self._overlay.apply_light_mode()

    @override
    def apply_dark_mode(self) -> None:
        super().apply_dark_mode()
        self.setStyleSheet(Background(border_radius=32, color=ColorBoxes.BLACK).to_stylesheet())
        self._body.apply_dark_mode()
        self._music_player.setStyleSheet("QWidget#musicPlayer{border-top: 1px solid #202020};border-radius:0px")
        self._music_player.apply_dark_mode()
        self._overlay.apply_dark_mode()

    def _set_default_playlist_cover(self, cover: bytes):
        self._body.set_default_playlist_cover(cover)

    @override
    def get_shortcut_map(self) -> dict[Shortcut, callable]:
        return self._overlay.get_shortcut_map()

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

    def add_alert(self, overlay: AlertDialog) -> None:
        self._overlay.add_alert(overlay)

    def add_confirm(self, overlay: ConfirmDialog) -> None:
        self._overlay.add_confirm(overlay)

    def add_dialog(self, overlay: Dialog) -> None:
        self._overlay.add_dialog(overlay)


class WindowOverlay(QWidget, BaseView, DialogWindow):
    __light_mode: bool = False
    __alert_dialog: AlertDialog = None
    __confirm_dialog: ConfirmDialog = None
    __dialog: Union[QWidget, BaseView] = None
    __higher_overlay: QWidget = None
    __lower_overlay: QWidget = None
    __shortcut_map: dict[Shortcut, callable] = {}

    def __init__(self, parent: Optional["QWidget"] = None):
        super().__init__(parent)
        self.__higher_overlay = QWidget(self)
        self.__higher_overlay.setGraphicsEffect(self.__create_effect())
        self.__higher_overlay.hide()

        self.__lower_overlay = QWidget(self)
        self.__lower_overlay.setGraphicsEffect(self.__create_effect())
        self.__lower_overlay.hide()

    @staticmethod
    def __create_effect():
        return QGraphicsDropShadowEffect(blurRadius=50,
                                         color=Colors.PRIMARY.with_opacity(
                                             25).to_QColor(),
                                         xOffset=0,
                                         yOffset=1)

    @override
    def apply_dark_mode(self) -> None:
        self.__light_mode = False
        if self.__alert_dialog is not None:
            self.__alert_dialog.apply_dark_mode()
        if self.__confirm_dialog is not None:
            self.__confirm_dialog.apply_dark_mode()
        if self.__dialog is not None:
            self.__dialog.apply_dark_mode()

    @override
    def apply_light_mode(self) -> None:
        self.__light_mode = True
        if self.__alert_dialog is not None:
            self.__alert_dialog.apply_light_mode()
        if self.__confirm_dialog is not None:
            self.__confirm_dialog.apply_light_mode()
        if self.__dialog is not None:
            self.__dialog.apply_light_mode()

    @override
    def get_shortcut_map(self) -> dict[Shortcut, callable]:
        return self.__shortcut_map

    @override
    def add_alert(self, widget: AlertDialog) -> None:
        self.__alert_dialog = widget
        self.__add_higher_dialog(widget)

    @override
    def add_confirm(self, widget: ConfirmDialog) -> None:
        self.__confirm_dialog = widget
        self.__add_higher_dialog(widget)

    def __add_higher_dialog(self, widget: Union[Dialog, QWidget]) -> None:
        if self.__light_mode:
            widget.apply_light_mode()
        else:
            widget.apply_dark_mode()
        widget.setParent(self.__higher_overlay)
        self.__move_to_center(widget)

        self.__add_short_cut_from_dialog(widget)
        widget.on_change_size(lambda: self.__move_to_center(widget))
        widget.on_close(lambda: self.__hide_higher_overlay(widget))

        widget.show()
        self.show()

        self.__higher_overlay.show()
        self.__higher_overlay.raise_()

    def __add_short_cut_from_dialog(self, widget):
        for shortcut in widget.get_shortcut_map():
            self.__shortcut_map[shortcut] = widget.get_shortcut_map()[shortcut]

    @override
    def add_dialog(self, widget: Dialog) -> None:
        self.__dialog = widget
        self.__add_lower_dialog(widget)

    def __add_lower_dialog(self, widget: Union[Dialog, QWidget]) -> None:
        if self.__light_mode:
            widget.apply_light_mode()
        else:
            widget.apply_dark_mode()
        widget.setParent(self.__lower_overlay)
        self.__move_to_center(widget)

        self.__add_short_cut_from_dialog(widget)
        widget.on_change_size(lambda: self.__move_to_center(widget))
        widget.on_close(lambda: self.__hide_lower_overlay(widget))

        widget.show()
        self.show()

        self.__lower_overlay.show()
        self.__lower_overlay.raise_()

    def __move_to_center(self, widget):
        widget.move(
            int(self.width() / 2 - widget.width() / 2),
            int(self.height() / 2 - widget.height() / 2),
        )

    def __hide_higher_overlay(self, widget: BaseView) -> None:
        if self.__confirm_dialog is not None and self.__confirm_dialog.isVisible():
            return

        if self.__alert_dialog is not None and self.__alert_dialog.isVisible():
            return

        self.__higher_overlay.hide()
        self.__hide_self()

        shortcut_map = widget.get_shortcut_map()
        self.__remove_shortcuts(shortcut_map)

    def __hide_lower_overlay(self, widget: BaseView) -> None:
        if self.__dialog is not None and self.__dialog.isVisible():
            return
        self.__lower_overlay.hide()
        self.__hide_self()
        shortcut_map = widget.get_shortcut_map()
        self.__remove_shortcuts(shortcut_map)

    def __remove_shortcuts(self, shortcut_map):
        for shortcut in shortcut_map:
            try:
                self.__shortcut_map.pop(shortcut)
            except Exception:
                pass

    def __hide_self(self):
        if self.__higher_overlay.isVisible() or self.__lower_overlay.isVisible():
            return
        return self.hide()
