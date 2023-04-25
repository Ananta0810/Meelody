from typing import Union, Optional, Callable

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLayout, QSystemTrayIcon, QAction, QMenu

from modules.helpers.types.Decorators import override, connector
from modules.models.view.builder.IconButtonStyle import IconButtonStyle
from modules.screens.AbstractScreen import BaseView
from modules.statics.view.Material import Paddings, Icons, Colors, Backgrounds
from modules.widgets.IconButton import IconButton


class FramelessWindow(QMainWindow, BaseView):
    __main_layout: QVBoxLayout
    __inner: QWidget
    __title_bar: QHBoxLayout
    __background: QWidget
    __btn_collapse: IconButton
    __btn_close: IconButton
    __btn_minimize: IconButton
    __title_bar_height: int = 72
    __offset: int = 0
    __onclick_collapse_fn: Callable[[], None] = None
    __onclick_close_fn: Callable[[], None] = None
    __onclick_minimize_fn: Callable[[], None] = None
    __icon_tray: QSystemTrayIcon
    __play_action_btn: QAction
    __onclick_play_fn: Callable[[], None]
    __onclick_pause_fn: Callable[[], None]
    __onclick_prev_fn: Callable[[], None]
    __onclick_next_fn: Callable[[], None]
    __is_playing: bool = False

    def __init__(self, parent: Optional["QWidget"] = None):
        super().__init__(parent)
        self.__init_component_ui()

    def __init_component_ui(self) -> None:
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowMinMaxButtonsHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.__background = QWidget(self)
        self.__inner = QWidget(self)
        self.setCentralWidget(self.__inner)

        self.__main_layout = QVBoxLayout(self.__inner)
        self.__main_layout.setContentsMargins(0, 0, 0, 0)
        self.__main_layout.setSpacing(0)

        self.__title_bar = QHBoxLayout()
        self.__title_bar.setContentsMargins(12, 12, 12, 12)
        self.__title_bar.setSpacing(8)

        self.__btn_collapse = IconButton.build(
            padding=Paddings.RELATIVE_50,
            size=Icons.MEDIUM,
            style=IconButtonStyle(
                light_mode_icon=Icons.MINIMIZE.with_color(Colors.PRIMARY),
                dark_mode_icon=Icons.MINIMIZE.with_color(Colors.WHITE),
                light_mode_background=Backgrounds.ROUNDED_HIDDEN_PRIMARY_25,
                dark_mode_background=Backgrounds.ROUNDED_HIDDEN_WHITE_50,
            )
        )

        self.__btn_minimize = IconButton.build(
            padding=Paddings.RELATIVE_50,
            size=Icons.MEDIUM,
            style=IconButtonStyle(
                light_mode_icon=Icons.MINIMIZE.with_color(Colors.PRIMARY),
                dark_mode_icon=Icons.MINIMIZE.with_color(Colors.WHITE),
                light_mode_background=Backgrounds.ROUNDED_HIDDEN_PRIMARY_25,
                dark_mode_background=Backgrounds.ROUNDED_HIDDEN_WHITE_50,
            )
        )

        self.__btn_close = IconButton.build(
            padding=Paddings.RELATIVE_50,
            size=Icons.MEDIUM,
            style=IconButtonStyle(
                light_mode_icon=Icons.CLOSE.with_color(Colors.DANGER),
                light_mode_background=Backgrounds.ROUNDED_DANGER_25,
                dark_mode_background=Backgrounds.ROUNDED_DANGER_25,
            )
        )

        self.__btn_collapse.clicked.connect(lambda: self.__click_collapse())
        self.__btn_minimize.clicked.connect(lambda: self.__click_minimize())
        self.__btn_close.clicked.connect(lambda: self.__click_close())

        self.__title_bar.addStretch()
        self.__title_bar.addWidget(self.__btn_collapse)
        self.__title_bar.addWidget(self.__btn_minimize)
        self.__title_bar.addWidget(self.__btn_close)

        self.__icon_tray = QSystemTrayIcon()
        self.__icon_tray.setIcon(Icons.LOGO)
        self.__icon_tray.setVisible(False)

        tray_menu = QMenu()

        show_action = QAction("Show", self)
        show_action.triggered.connect(lambda: self.__set_collapse(False))
        tray_menu.addAction(show_action)

        self.__play_action_btn = QAction(self)
        self.__play_action_btn.triggered.connect(lambda: self.__onclick_pause())
        tray_menu.addAction(self.__play_action_btn)

        prev_action = QAction("Previous song", self)
        prev_action.triggered.connect(lambda: self.__onclick_prev_fn())
        tray_menu.addAction(prev_action)

        next_action = QAction("Next song", self)
        next_action.triggered.connect(lambda: self.__onclick_next_fn())
        tray_menu.addAction(next_action)

        self.__icon_tray.setContextMenu(tray_menu)
        self.__icon_tray.show()

        self.addLayout(self.__title_bar)

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
        self.__play_action_btn.setText("Pause" if is_playing else "Play")

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

    def with_title_bar_height(self, height: int) -> 'FramelessWindow':
        self.__title_bar_height = height
        return self

    def show_minimize_button(self, enable: bool) -> None:
        self.__btn_minimize.setVisible(enable)

    def show_close_button(self, enable: bool) -> None:
        self.__btn_close.setVisible(enable)

    def __set_collapse(self, collapse: bool) -> None:
        if collapse:
            self.hide()
        else:
            self.show()

    @connector
    def set_onclick_collapse(self, fn: Callable[[], None]) -> None:
        self.__onclick_collapse_fn = fn

    def __click_collapse(self):
        self.__set_collapse(True)
        self.__icon_tray.setVisible(True)
        if self.__onclick_collapse_fn is not None:
            self.__onclick_collapse_fn()

    @connector
    def set_onclick_close(self, fn: Callable[[], None]) -> None:
        self.__onclick_close_fn = fn

    @connector
    def set_onclick_minimize(self, fn: Callable[[], None]) -> None:
        self.__onclick_minimize_fn = fn

    def __click_minimize(self) -> None:
        self.showMinimized()
        if self.__onclick_minimize_fn is not None:
            self.__onclick_minimize_fn()

    def __click_close(self) -> None:
        self.close()
        if self.__onclick_close_fn is not None:
            self.__onclick_close_fn()

    @override
    def apply_light_mode(self) -> None:
        self.__btn_collapse.apply_light_mode()
        self.__btn_minimize.apply_light_mode()
        self.__btn_close.apply_light_mode()

    @override
    def apply_dark_mode(self) -> None:
        self.__btn_collapse.apply_dark_mode()
        self.__btn_minimize.apply_dark_mode()
        self.__btn_close.apply_dark_mode()

    @override
    def resizeEvent(self, event: QResizeEvent) -> None:
        self.__background.resize(self.size())
        return super().resizeEvent(event)

    @override
    def addLayout(self, widget: QLayout) -> None:
        self.__main_layout.addLayout(widget)

    @override
    def addWidget(
        self,
        layout: QWidget,
        stretch: int = 0,
        alignment: Union[Qt.Alignment, Qt.AlignmentFlag] = None
    ) -> None:
        if alignment is None:
            self.__main_layout.addWidget(layout, stretch=stretch)
            return
        self.__main_layout.addWidget(layout, stretch=stretch, alignment=alignment)

    @override
    def setStyleSheet(self, style_sheet: str) -> None:
        self.__background.setStyleSheet(style_sheet)

    @override
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.pos().y() < self.__title_bar_height and event.button() == Qt.LeftButton:
            self.__offset = event.pos()

    @override
    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.__offset = 0

    @override
    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if self.__offset == 0:
            return
        delta = event.pos() - self.__offset
        self.move(self.pos() + delta)
