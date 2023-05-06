from typing import Callable

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

from modules.helpers.types.Decorators import override
from modules.models.view.Border import Border
from modules.models.view.Color import Color
from modules.models.view.ColorBox import ColorBox
from modules.models.view.builder.FontBuilder import FontBuilder
from modules.models.view.builder.IconButtonStyle import IconButtonStyle
from modules.models.view.builder.TextStyle import TextStyle
from modules.screens.AbstractScreen import BaseView
from modules.statics.view.Material import Backgrounds, Colors, Paddings, Icons, ColorBoxes
from modules.widgets.Buttons import IconButton, ActionButton
from modules.widgets.Cover import CoverProp, Cover
from modules.widgets.FramelessWindow import FramelessWindow
from modules.widgets.Labels import LabelWithDefaultText


class BaseDialog(FramelessWindow, BaseView):
    __on_close_fn: callable = None
    __on_change_size_fn: callable = None

    def __init__(self):
        super().__init__()
        self.setWindowModality(Qt.ApplicationModal)
        self.apply_light_mode()

    def _add_body_to(self, parent: QWidget) -> None:
        parent.setContentsMargins(24, 24, 24, 24)
        self.__background = QWidget(parent)

        self._btn_close = IconButton.build(
            padding=Paddings.RELATIVE_50,
            size=Icons.MEDIUM,
            style=IconButtonStyle(
                light_mode_icon=Icons.CLOSE.with_color(Colors.GRAY),
                light_mode_background=Backgrounds.ROUNDED_HIDDEN_GRAY_25
            ),
            parent=parent
        )
        self._btn_close.clicked.connect(self.close)
        self._build_content(parent)

    def _build_content(self, parent: QWidget) -> None:
        ...

    @override
    def resizeEvent(self, event: QResizeEvent) -> None:
        self.__background.resize(self.size())
        self._btn_close.move(self.size().width() - self._btn_close.width() - 4, 4)
        if self.__on_change_size_fn is not None:
            self.__on_change_size_fn()

    @override
    def apply_dark_mode(self) -> None:
        self.__background.setStyleSheet(Backgrounds.ROUNDED_BLACK.with_border_radius(12).to_stylesheet())
        self._btn_close.apply_dark_mode()

    @override
    def apply_light_mode(self) -> None:
        self.__background.setStyleSheet(Backgrounds.ROUNDED_WHITE.with_border_radius(12).to_stylesheet())
        self._btn_close.apply_light_mode()


class AlertDialog(BaseDialog, BaseView):
    _onclick_accept_fn: Callable[[], bool]

    def _build_content(self, parent: QWidget) -> None:
        self.__image = Cover()
        self.__image.setAlignment(Qt.AlignHCenter)

        self.__header = LabelWithDefaultText.build(
            font=FontBuilder.build(family="Segoe UI Semibold", size=16, bold=True),
            light_mode_style=TextStyle(text_color=ColorBoxes.BLACK),
            dark_mode_style=TextStyle(text_color=ColorBoxes.WHITE),
            allow_multiple_lines=True
        )
        self.__header.setAlignment(Qt.AlignCenter)

        self.__message = LabelWithDefaultText.build(
            font=FontBuilder.build(size=11),
            light_mode_style=TextStyle(text_color=ColorBoxes.BLACK),
            dark_mode_style=TextStyle(text_color=ColorBoxes.WHITE),
            allow_multiple_lines=True
        )
        self.__message.setAlignment(Qt.AlignCenter)

        self.__button_box = QHBoxLayout()
        self.__button_box.setContentsMargins(0, 0, 0, 0)

        self.__accept_btn = ActionButton.build(
            font=FontBuilder.build(size=12, family="Segoe UI Semibold"),
            size=QSize(0, 48),
            light_mode=TextStyle(text_color=ColorBoxes.WHITE,
                                 background=Backgrounds.ROUNDED_PRIMARY_75.with_border_radius(8)),
            dark_mode=TextStyle(text_color=ColorBoxes.WHITE, background=Backgrounds.ROUNDED_WHITE_25)
        )
        self.__accept_btn.clicked.connect(self.close)
        self.__button_box.addWidget(self.__accept_btn)

        self.__view_layout = QVBoxLayout(parent)
        self.__view_layout.setAlignment(Qt.AlignVCenter)
        self.__view_layout.setSpacing(12)

        self.__view_layout.addWidget(self.__image)
        self.__view_layout.addWidget(self.__header)
        self.__view_layout.addWidget(self.__message)
        self.__view_layout.addLayout(self.__button_box)
        self.setFixedWidth(360)
        self._btn_close.hide()

    def set_info(self, image: bytes, header: str, message: str, accept_text: str) -> None:
        self.__image.set_cover(CoverProp.from_bytes(image, width=128))
        self.__header.setText(header)
        self.__message.setText(message)
        self.__accept_btn.setText(accept_text)
        self.setMaximumHeight(self.sizeHint().height())

    @override
    def apply_dark_mode(self) -> None:
        super().apply_dark_mode()
        self.__header.apply_dark_mode()
        self.__message.apply_dark_mode()
        self.__accept_btn.apply_dark_mode()

    @override
    def apply_light_mode(self) -> None:
        super().apply_light_mode()
        self.__header.apply_light_mode()
        self.__message.apply_light_mode()
        self.__accept_btn.apply_light_mode()


class ConfirmDialog(BaseDialog, BaseView):
    __on_accept_fn: callable = None
    __on_cancel_fn: callable = None

    def _build_content(self, parent: QWidget) -> None:
        self.__image = Cover()
        self.__image.setAlignment(Qt.AlignHCenter)

        self.__header = LabelWithDefaultText.build(
            font=FontBuilder.build(family="Segoe UI Semibold", size=16, bold=True),
            light_mode_style=TextStyle(text_color=ColorBoxes.BLACK),
            dark_mode_style=TextStyle(text_color=ColorBoxes.WHITE),
            allow_multiple_lines=True
        )
        self.__header.setAlignment(Qt.AlignCenter)

        self.__message = LabelWithDefaultText.build(
            font=FontBuilder.build(size=11),
            light_mode_style=TextStyle(text_color=ColorBoxes.BLACK),
            dark_mode_style=TextStyle(text_color=ColorBoxes.WHITE),
            allow_multiple_lines=True
        )
        self.__message.setAlignment(Qt.AlignCenter)

        self.__button_box = QHBoxLayout()

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
        self.__cancel_btn.clicked.connect(lambda: self._on_cancel())
        self.__button_box.addWidget(self.__cancel_btn)

        self.__accept_btn = ActionButton.build(
            font=FontBuilder.build(family="Segoe UI Semibold", size=11),
            size=QSize(0, 48),
            light_mode=TextStyle(text_color=ColorBoxes.WHITE,
                                 background=Backgrounds.ROUNDED_DANGER_75.with_border_radius(8)),
            dark_mode=TextStyle(text_color=ColorBoxes.WHITE, background=Backgrounds.ROUNDED_WHITE_25)
        )
        self.__accept_btn.clicked.connect(self.close)
        self.__button_box.addWidget(self.__accept_btn)

        self.__view_layout = QVBoxLayout(parent)
        self.__view_layout.setAlignment(Qt.AlignVCenter)
        self.__view_layout.addWidget(self.__image)
        self.__view_layout.addWidget(self.__header)
        self.__view_layout.addWidget(self.__message)
        self.__view_layout.addSpacing(8)
        self.__view_layout.addLayout(self.__button_box)

        self.setFixedWidth(360)
        self._btn_close.hide()

    def set_info(self,
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
        self.setMaximumHeight(self.sizeHint().height())

    @override
    def apply_dark_mode(self) -> None:
        super().apply_dark_mode()
        self.__header.apply_dark_mode()
        self.__message.apply_dark_mode()
        self.__cancel_btn.apply_dark_mode()
        self.__accept_btn.apply_dark_mode()

    @override
    def apply_light_mode(self) -> None:
        super().apply_light_mode()
        self.__header.apply_light_mode()
        self.__message.apply_light_mode()
        self.__cancel_btn.apply_light_mode()
        self.__accept_btn.apply_light_mode()
