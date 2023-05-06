from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QResizeEvent, QShowEvent
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QGraphicsDropShadowEffect

from modules.helpers.types.Decorators import override
from modules.models.view.Border import Border
from modules.models.view.Color import Color
from modules.models.view.ColorBox import ColorBox
from modules.models.view.builder.FontBuilder import FontBuilder
from modules.models.view.builder.IconButtonStyle import IconButtonStyle
from modules.models.view.builder.TextStyle import TextStyle
from modules.screens.AbstractScreen import BaseView
from modules.statics.view.Material import Backgrounds, ColorBoxes, Paddings, Icons, Colors
from modules.widgets.Buttons import ActionButton, IconButton
from modules.widgets.Cover import CoverProp, Cover
from modules.widgets.Labels import LabelWithDefaultText
from modules.widgets.Windows import FramelessWindow


def alert(
    image: bytes,
    header: str,
    message: str,
    acceptText: str = "OK",
) -> None:
    dialog = _AlertDialog()
    dialog.setInfo(image, header, message, acceptText)
    dialog.apply_light_mode()
    dialog.exec_()


def confirm(
    image: bytes,
    header: str,
    message: str,
    acceptText: str = "OK",
    cancelText: str = "Cancel",
    on_accept: callable = None,
    on_cancel: callable = None
) -> None:
    dialog = _ConfirmDialog()
    dialog.setInfo(image, header, message, acceptText, cancelText)

    if on_accept is not None:
        dialog.accepted.connect(on_accept)
    if on_cancel is not None:
        dialog.canceled.connect(on_cancel)

    dialog.apply_light_mode()
    dialog.exec_()


class Dialog(FramelessWindow, BaseView):
    __on_close_fn: callable = None
    __on_change_size_fn: callable = None

    def __init__(self):
        super().__init__()
        self.__init_ui()

    def __init_ui(self) -> None:
        self.__layout = QHBoxLayout()
        self._btn_close = IconButton.build(
            padding=Paddings.RELATIVE_50,
            size=Icons.MEDIUM,
            style=IconButtonStyle(
                light_mode_icon=Icons.CLOSE.with_color(Colors.GRAY),
                light_mode_background=Backgrounds.ROUNDED_HIDDEN_GRAY_25
            )
        )
        self.__layout.addStretch(1)
        self.__layout.addWidget(self._btn_close)
        self.addLayout(self.__layout)
        self._btn_close.clicked.connect(self.close)
        self.__layout.setContentsMargins(8, 8, 8, 0)

        self._build_content()
        self.setWindowModality(Qt.ApplicationModal)

    def _build_content(self) -> None:
        ...

    def showEvent(self, a0: QShowEvent) -> None:
        super().showEvent(a0)
        self.moveToCenter()

    @override
    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        self._btn_close.move(self.width() - self._btn_close.width() - 4, 4)
        if self.__on_change_size_fn is not None:
            self.__on_change_size_fn()
        self.setFixedHeight(self.height())
        print(self.width())
        print(self.height())

    @override
    def apply_dark_mode(self) -> None:
        self.setStyleSheet(Backgrounds.ROUNDED_BLACK.with_border_radius(12).to_stylesheet())
        self._btn_close.apply_dark_mode()

    @override
    def apply_light_mode(self) -> None:
        self.setStyleSheet(Backgrounds.ROUNDED_WHITE.with_border_radius(12).to_stylesheet())
        self._btn_close.apply_light_mode()


class _AlertDialog(QtWidgets.QDialog, BaseView):

    def __init__(self) -> None:
        super().__init__()
        self.__background = QWidget(self)
        self.__inner = QWidget(self)
        self.__view_layout = QVBoxLayout(self.__inner)

        self.__image = Cover()
        self.__header = LabelWithDefaultText.build(
            font=FontBuilder.build(family="Segoe UI Semibold", size=16, bold=True),
            light_mode_style=TextStyle(text_color=ColorBoxes.BLACK),
            dark_mode_style=TextStyle(text_color=ColorBoxes.WHITE),
        )

        self.__message = LabelWithDefaultText.build(
            font=FontBuilder.build(size=11),
            light_mode_style=TextStyle(text_color=ColorBoxes.BLACK),
            dark_mode_style=TextStyle(text_color=ColorBoxes.WHITE),
            allow_multiple_lines=True
        )

        self.__accept_btn = ActionButton.build(
            font=FontBuilder.build(family="Segoe UI Semibold", size=11),
            size=QSize(0, 48),
            light_mode=TextStyle(text_color=ColorBoxes.WHITE,
                                 background=Backgrounds.ROUNDED_PRIMARY_75.with_border_radius(8)),
            dark_mode=TextStyle(text_color=ColorBoxes.WHITE, background=Backgrounds.ROUNDED_WHITE_25)
        )

        self.__initUi()
        self.connectToSignalSlot()

    def __initUi(self) -> None:
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowMinMaxButtonsHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowModality(Qt.ApplicationModal)

        shadow = QGraphicsDropShadowEffect(
            blurRadius=32, color=Colors.PRIMARY.with_alpha(75).to_QColor(), xOffset=0, yOffset=3
        )
        self.setGraphicsEffect(shadow)

        self.__inner.move(32, 32)
        self.__background.move(32, 32)
        self.__background.setAutoFillBackground(True)

        self.__image.setAlignment(Qt.AlignHCenter)
        self.__header.setAlignment(Qt.AlignCenter)
        self.__message.setAlignment(Qt.AlignCenter)

        self.__inner.setContentsMargins(24, 24, 24, 24)
        self.__view_layout.setContentsMargins(0, 0, 0, 0)
        self.__view_layout.setAlignment(Qt.AlignVCenter)
        self.__view_layout.addWidget(self.__image)
        self.__view_layout.addWidget(self.__header)
        self.__view_layout.addWidget(self.__message)
        self.__view_layout.addWidget(self.__accept_btn)

    def connectToSignalSlot(self):
        self.__accept_btn.clicked.connect(self.close)

    @override
    def setFixedSize(self, w: int, h: int) -> None:
        margins = self.__inner.contentsMargins()
        super().setFixedSize(w + margins.left() + margins.right(), h + margins.top() + margins.bottom())
        self.__inner.setFixedSize(w, h)
        self.__background.setFixedSize(w, h)

    def setInfo(self, image: bytes, header: str, message: str, accept_text: str) -> None:
        self.__image.set_cover(CoverProp.from_bytes(image, width=128))
        self.__header.setText(header)
        self.__message.setText(message)
        self.__accept_btn.setText(accept_text)
        self.setMaximumHeight(self.sizeHint().height())
        self.setFixedSize(360, self.__inner.sizeHint().height())

    @override
    def apply_dark_mode(self) -> None:
        self.setStyleSheet(Backgrounds.ROUNDED_BLACK.with_border_radius(12).to_stylesheet())
        self.__header.apply_dark_mode()
        self.__message.apply_dark_mode()
        self.__accept_btn.apply_dark_mode()

    @override
    def apply_light_mode(self) -> None:
        self.setStyleSheet(Backgrounds.ROUNDED_WHITE.with_border_radius(12).to_stylesheet())
        self.__header.apply_light_mode()
        self.__message.apply_light_mode()
        self.__accept_btn.apply_light_mode()


class _ConfirmDialog(QtWidgets.QDialog, BaseView):
    canceled: pyqtSignal() = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.__background = QWidget(self)
        self.__inner = QWidget(self)
        self.__view_layout = QVBoxLayout(self.__inner)

        self.__image = Cover()
        self.__header = LabelWithDefaultText.build(
            font=FontBuilder.build(family="Segoe UI Semibold", size=16, bold=True),
            light_mode_style=TextStyle(text_color=ColorBoxes.BLACK),
            dark_mode_style=TextStyle(text_color=ColorBoxes.WHITE),
            allow_multiple_lines=True
        )
        self.__message = LabelWithDefaultText.build(
            font=FontBuilder.build(size=11),
            light_mode_style=TextStyle(text_color=ColorBoxes.BLACK),
            dark_mode_style=TextStyle(text_color=ColorBoxes.WHITE),
            allow_multiple_lines=True
        )
        self.__button_box = QHBoxLayout()

        self.__accept_btn = ActionButton.build(
            font=FontBuilder.build(family="Segoe UI Semibold", size=11),
            size=QSize(0, 48),
            light_mode=TextStyle(text_color=ColorBoxes.WHITE,
                                 background=Backgrounds.ROUNDED_DANGER_75.with_border_radius(8)),
            dark_mode=TextStyle(text_color=ColorBoxes.WHITE, background=Backgrounds.ROUNDED_WHITE_25)
        )
        self.__cancel_btn = ActionButton.build(
            font=FontBuilder.build(family="Segoe UI Semibold", size=11),
            size=QSize(0, 48),
            light_mode=TextStyle(text_color=ColorBoxes.BLACK,
                                 background=Backgrounds.ROUNDED_WHITE
                                 .with_border_radius(8)
                                 .with_border(
                                     Border(size=2, color=ColorBox(Color(216, 216, 216), Color(192, 192, 192)))),
                                 ),
            dark_mode=TextStyle(text_color=ColorBoxes.WHITE, background=Backgrounds.ROUNDED_WHITE_25)
        )

        self.__initUi()
        self.connectToSignalSlot()

    def __initUi(self) -> None:
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowMinMaxButtonsHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowModality(Qt.ApplicationModal)

        shadow = QGraphicsDropShadowEffect(
            blurRadius=32, color=Colors.PRIMARY.with_alpha(75).to_QColor(), xOffset=0, yOffset=3
        )
        self.setGraphicsEffect(shadow)

        self.__inner.move(32, 32)
        self.__background.move(32, 32)
        self.__background.setAutoFillBackground(True)

        self.__image.setAlignment(Qt.AlignHCenter)
        self.__header.setAlignment(Qt.AlignCenter)
        self.__message.setAlignment(Qt.AlignCenter)

        self.__button_box.addWidget(self.__accept_btn)
        self.__button_box.addWidget(self.__cancel_btn)

        self.__inner.setContentsMargins(24, 24, 24, 24)
        self.__view_layout.setContentsMargins(0, 0, 0, 0)
        self.__view_layout.setAlignment(Qt.AlignVCenter)
        self.__view_layout.addWidget(self.__image)
        self.__view_layout.addWidget(self.__header)
        self.__view_layout.addWidget(self.__message)
        self.__view_layout.addSpacing(8)
        self.__view_layout.addLayout(self.__button_box)

    def connectToSignalSlot(self):
        self.__cancel_btn.clicked.connect(self.canceled.emit)
        self.__accept_btn.clicked.connect(self.accepted.emit)
        self.accepted.connect(self.close)
        self.canceled.connect(self.close)

    @override
    def setFixedSize(self, w: int, h: int) -> None:
        margins = self.__inner.contentsMargins()
        super().setFixedSize(w + margins.left() + margins.right(), h + margins.top() + margins.bottom())
        self.__inner.setFixedSize(w, h)
        self.__background.setFixedSize(w, h)

    def setInfo(self,
                image: bytes,
                header: str,
                message: str,
                accept_text: str,
                cancel_text: str
                ) -> None:
        self.__image.set_cover(CoverProp.from_bytes(image, width=128))
        self.__header.setText(header)
        self.__message.setText(message)
        self.__accept_btn.setText(accept_text)
        self.__cancel_btn.setText(cancel_text)
        self.setFixedSize(360, self.__inner.sizeHint().height())

    @override
    def apply_dark_mode(self) -> None:
        self.setStyleSheet(Backgrounds.ROUNDED_BLACK.with_border_radius(12).to_stylesheet())
        self.__header.apply_dark_mode()
        self.__message.apply_dark_mode()
        self.__cancel_btn.apply_dark_mode()
        self.__accept_btn.apply_dark_mode()

    @override
    def apply_light_mode(self) -> None:
        self.setStyleSheet(Backgrounds.ROUNDED_WHITE.with_border_radius(12).to_stylesheet())
        self.__header.apply_light_mode()
        self.__message.apply_light_mode()
        self.__cancel_btn.apply_light_mode()
        self.__accept_btn.apply_light_mode()
