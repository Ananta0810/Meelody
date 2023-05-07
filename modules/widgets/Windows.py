from typing import Callable, overload, Union

from PyQt5.QtCore import Qt, QSize, QMargins
from PyQt5.QtGui import QResizeEvent, QMouseEvent, QShowEvent
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QDesktopWidget, QMainWindow, \
    QGraphicsDropShadowEffect, QLayout

from modules.helpers.types.Decorators import override, connector
from modules.models.view.builder.IconButtonStyle import IconButtonStyle
from modules.screens.AbstractScreen import BaseView
from modules.statics.view.Material import Paddings, Icons, Colors, Backgrounds
from modules.widgets.Buttons import IconButton


class FramelessWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.__titleBarHeight: int = 72
        self.__offset: int = 0

        self.__outer = QWidget()

        self.__background = QWidget(self.__outer)
        self.__inner = QWidget(self.__outer)
        self.__main_layout = QVBoxLayout(self.__inner)

        self.__init_ui()

    def __init_ui(self) -> None:
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowMinMaxButtonsHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setCentralWidget(self.__outer)

        shadow = QGraphicsDropShadowEffect(blurRadius=32,
                                           color=Colors.PRIMARY.with_alpha(33).to_QColor(),
                                           xOffset=0,
                                           yOffset=3)
        self.__outer.setGraphicsEffect(shadow)

        self.__inner.move(32, 32)
        self.__background.move(32, 32)
        self.__background.setAutoFillBackground(True)

        self.__main_layout.setContentsMargins(0, 0, 0, 0)
        self.__main_layout.setSpacing(0)

    def setTitleHeight(self, height: int) -> None:
        self.__titleBarHeight = height

    def moveToCenter(self):
        qtRectangle = self.__outer.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

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
    def setFixedHeight(self, h: int) -> None:
        self.__background.setFixedHeight(h)
        self.__inner.setFixedHeight(h)
        self.__outer.setFixedSize(self.__inner.width() + 64, self.__inner.height() + 64)

    @override
    def setFixedWidth(self, w: int) -> None:
        self.__background.setFixedWidth(w)
        self.__inner.setFixedWidth(w)
        self.__outer.setFixedSize(self.__inner.width() + 64, self.__inner.height() + 64)

    @overload
    @override
    def setFixedSize(self, a0: QSize) -> None:
        self.__background.setFixedWidth(a0)
        self.__inner.setFixedWidth(a0)
        self.__outer.setFixedSize(self.__inner.width() + 64, self.__inner.height() + 64)

    @overload
    @override
    def setFixedSize(self, w: int, h: int) -> None:
        self.__background.setFixedWidth(w, h)
        self.__inner.setFixedWidth(w, h)
        self.__outer.setFixedSize(self.__inner.width() + 64, self.__inner.height() + 64)

    @override
    def setFixedSize(self, a0: QSize) -> None:
        self.__background.setFixedSize(a0)
        self.__inner.setFixedSize(a0)
        self.__outer.setFixedSize(self.__inner.width() + 64, self.__inner.height() + 64)

    @override
    def width(self) -> int:
        return self.__inner.sizeHint().width()

    @override
    def height(self) -> int:
        return self.__inner.sizeHint().height()

    @overload
    @override
    def setContentsMargins(self, left: int, top: int, right: int, bottom: int) -> None:
        self.__background.setContentsMargins(left, top, right, bottom)
        self.__inner.setContentsMargins(left, top, right, bottom)

    @overload
    @override
    def setContentsMargins(self, margins: QMargins) -> None:
        self.__background.setContentsMargins(margins)
        self.__inner.setContentsMargins(margins)

    @override
    def setContentsMargins(self, left: int, top: int, right: int, bottom: int) -> None:
        self.__background.setContentsMargins(left, top, right, bottom)
        self.__inner.setContentsMargins(left, top, right, bottom)

    def showEvent(self, a0: QShowEvent) -> None:
        super().showEvent(a0)
        self.__outer.setFixedSize(self.__inner.width() + 64, self.__inner.height() + 64)

    @override
    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        self.__background.resize(self.size())
        height_ = self.__inner.height() + 64
        self.__outer.setFixedSize(self.__inner.width() + 64, height_)

    @override
    def mousePressEvent(self, event: QMouseEvent) -> None:
        super().mousePressEvent(event)
        if event.pos().y() < self.__titleBarHeight and event.button() == Qt.LeftButton:
            self.__offset = event.pos()

    @override
    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        super().mouseReleaseEvent(event)
        self.__offset = 0

    @override
    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        super().mouseMoveEvent(event)
        if self.__offset == 0:
            return
        delta = event.pos() - self.__offset
        self.move(self.pos() + delta)

    @override
    def setStyleSheet(self, style: str) -> None:
        self.__background.setStyleSheet(style)


class CloseableWindow(FramelessWindow, BaseView):
    __title_bar: QHBoxLayout
    __btn_close: IconButton
    __btn_minimize: IconButton
    __onclick_collapse_fn: Callable[[], None] = None
    __on_exit_fn: Callable[[], None] = None
    __onclick_minimize_fn: Callable[[], None] = None

    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self) -> None:
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

        self.addLayout(self.__title_bar)

    @override
    def apply_light_mode(self) -> None:
        self.__btn_minimize.apply_light_mode()
        self.__btn_close.apply_light_mode()

    @override
    def apply_dark_mode(self) -> None:
        self.__btn_minimize.apply_dark_mode()
        self.__btn_close.apply_dark_mode()

    @connector
    def set_onclick_collapse(self, fn: Callable[[], None]) -> None:
        self.__onclick_collapse_fn = fn

    @connector
    def set_on_exit(self, fn: Callable[[], None]) -> None:
        self.__on_exit_fn = fn

    @connector
    def set_onclick_minimize(self, fn: Callable[[], None]) -> None:
        self.__onclick_minimize_fn = fn

    def __click_collapse(self):
        self.hide()
        if self.__onclick_collapse_fn is not None:
            self.__onclick_collapse_fn()

    def __click_minimize(self) -> None:
        self.showMinimized()
        if self.__onclick_minimize_fn is not None:
            self.__onclick_minimize_fn()

    def __exit(self) -> None:
        self.close()
        if self.__on_exit_fn is not None:
            self.__on_exit_fn()

    def show_minimize_button(self, enable: bool) -> None:
        self.__btn_minimize.setVisible(enable)

    def show_close_button(self, enable: bool) -> None:
        self.__btn_close.setVisible(enable)
