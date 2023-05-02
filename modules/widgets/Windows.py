from typing import Union, Optional, Callable

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLayout, QSystemTrayIcon, QAction, QMenu, \
    QGraphicsDropShadowEffect

from modules.helpers.types.Decorators import override, connector
from modules.models.view.builder.IconButtonStyle import IconButtonStyle
from modules.screens.AbstractScreen import BaseView
from modules.statics.view.Material import Paddings, Icons, Colors, Backgrounds
from modules.widgets.Buttons import IconButton
from modules.widgets.DialogWindow import DialogWindow
from modules.widgets.Dialogs import AlertDialog, ConfirmDialog, Dialog


class FramelessWindow(QMainWindow, DialogWindow, BaseView):
    __main_layout: QVBoxLayout
    __inner: QWidget
    __title_bar: QHBoxLayout
    __background: QWidget
    __btn_close: IconButton
    __btn_minimize: IconButton
    __title_bar_height: int = 72
    __offset: int = 0
    __onclick_collapse_fn: Callable[[], None] = None
    __on_exit_fn: Callable[[], None] = None
    __onclick_minimize_fn: Callable[[], None] = None
    __tray: QSystemTrayIcon
    __play_action_btn: QAction
    __onclick_play_fn: Callable[[], None]
    __onclick_pause_fn: Callable[[], None]
    __onclick_prev_fn: Callable[[], None]
    __onclick_next_fn: Callable[[], None]
    __is_playing: bool = False

    def __init__(self, parent: Optional["QWidget"] = None):
        super().__init__(parent)
        self.__init_ui()
        self.__overlay.hide()
        self.__tray.setVisible(False)

    def __init_ui(self) -> None:
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

        self.__btn_minimize.clicked.connect(lambda: self.__click_minimize())
        self.__btn_close.clicked.connect(lambda: self.__click_collapse())

        self.__title_bar.addStretch()
        self.__title_bar.addWidget(self.__btn_minimize)
        self.__title_bar.addWidget(self.__btn_close)

        self.__tray = QSystemTrayIcon()
        self.__tray.setIcon(Icons.LOGO)
        self.__tray.setToolTip("Meelody")

        tray_menu = QMenu()
        tray_menu.setStyleSheet(
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

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(lambda: self.__exit())
        tray_menu.addAction(exit_action)

        self.__tray.setContextMenu(tray_menu)

        self.addLayout(self.__title_bar)
        self.__overlay = WindowOverlay(self.__inner)

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

    def __clicked_show_btn(self) -> None:
        self.show()
        self.__tray.hide()

    @connector
    def set_onclick_collapse(self, fn: Callable[[], None]) -> None:
        self.__onclick_collapse_fn = fn

    def __click_collapse(self):
        self.hide()
        self.__tray.setVisible(True)
        if self.__onclick_collapse_fn is not None:
            self.__onclick_collapse_fn()

    @connector
    def set_on_exit(self, fn: Callable[[], None]) -> None:
        self.__on_exit_fn = fn

    @connector
    def set_onclick_minimize(self, fn: Callable[[], None]) -> None:
        self.__onclick_minimize_fn = fn

    def __click_minimize(self) -> None:
        self.showMinimized()
        self.__tray.show()
        if self.__onclick_minimize_fn is not None:
            self.__onclick_minimize_fn()

    def __exit(self) -> None:
        self.close()
        if self.__on_exit_fn is not None:
            self.__on_exit_fn()

    @override
    def apply_light_mode(self) -> None:
        self.__btn_minimize.apply_light_mode()
        self.__btn_close.apply_light_mode()
        self.__overlay.apply_light_mode()

    @override
    def apply_dark_mode(self) -> None:
        self.__btn_minimize.apply_dark_mode()
        self.__btn_close.apply_dark_mode()
        self.__overlay.apply_dark_mode()

    @override
    def resizeEvent(self, event: QResizeEvent) -> None:
        self.__background.resize(self.size())
        self.__overlay.resize(self.size())
        self.__overlay.raise_()
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

    def add_alert(self, overlay: AlertDialog) -> None:
        self.__overlay.add_alert(overlay)

    def add_confirm(self, overlay: ConfirmDialog) -> None:
        self.__overlay.add_confirm(overlay)

    def add_dialog(self, overlay: Dialog) -> None:
        self.__overlay.add_dialog(overlay)


class WindowOverlay(QWidget, BaseView, DialogWindow):
    __light_mode: bool = False
    __alert_dialog: AlertDialog = None
    __confirm_dialog: ConfirmDialog = None
    __dialog: Union[QWidget, BaseView] = None
    __higher_overlay: QWidget = None
    __lower_overlay: QWidget = None

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

        widget.on_change_size(lambda: self.__move_to_center(widget))
        widget.on_close(lambda: self.__hide_higher_overlay())

        widget.show()
        self.show()

        self.__higher_overlay.show()
        self.__higher_overlay.raise_()

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

        widget.on_change_size(lambda: self.__move_to_center(widget))
        widget.on_close(lambda: self.__hide_lower_overlay())

        widget.show()
        self.show()

        self.__lower_overlay.show()
        self.__lower_overlay.raise_()

    def __move_to_center(self, widget):
        widget.move(
            int(self.width() / 2 - widget.width() / 2),
            int(self.height() / 2 - widget.height() / 2),
        )

    def __hide_higher_overlay(self):
        if self.__confirm_dialog is not None and self.__confirm_dialog.isVisible():
            return

        if self.__alert_dialog is not None and self.__alert_dialog.isVisible():
            return

        self.__higher_overlay.hide()
        self.__hide_self()

    def __hide_lower_overlay(self):
        if self.__dialog is not None and self.__dialog.isVisible():
            return
        self.__lower_overlay.hide()
        self.__hide_self()

    def __hide_self(self):
        if self.__higher_overlay.isVisible() or self.__lower_overlay.isVisible():
            return
        return self.hide()
