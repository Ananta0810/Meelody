from abc import abstractmethod
from typing import Callable

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout

from modules.helpers.types.Decorators import override, connector
from modules.helpers.types.Metas import SingletonMeta
from modules.models.view.Border import Border
from modules.models.view.Color import Color
from modules.models.view.ColorBox import ColorBox
from modules.models.view.builder.FontBuilder import FontBuilder
from modules.models.view.builder.IconButtonStyle import IconButtonStyle
from modules.models.view.builder.TextStyle import TextStyle
from modules.screens.AbstractScreen import BaseView
from modules.statics.view.Material import ColorBoxes, Backgrounds, Colors, Paddings, Icons
from modules.widgets.Buttons import ActionButton, IconButton
from modules.widgets.Cover import Cover, CoverProp
from modules.widgets.DialogWindow import DialogWindow
from modules.widgets.Labels import LabelWithDefaultText


class Dialogs(metaclass=SingletonMeta):
    __alert: 'AlertDialog' = None
    __confirm: 'ConfirmDialog' = None
    __window: DialogWindow = None

    def set_alert(self, dialog: 'AlertDialog') -> None:
        self.__alert = dialog

    def set_window(self, window: 'DialogWindow') -> None:
        self.__window = window

    def set_confirm(self, dialog: 'ConfirmDialog') -> None:
        self.__confirm = dialog

    def alert(self,
              with_image: bytes,
              with_header: str,
              with_message: str,
              with_accept_text: str = "OK",
              ) -> None:
        self.__alert.set_info(with_image, with_header, with_message, with_accept_text)
        self.__alert.show()

    def confirm(self,
                image: bytes,
                header: str,
                message: str,
                accept_text: str = "OK",
                cancel_text: str = "Cancel",
                on_accept: callable = None,
                on_cancel: callable = None
                ) -> None:
        self.__confirm.set_info(image, header, message, accept_text, cancel_text)
        self.__confirm.on_accept(on_accept)
        self.__confirm.on_cancel(on_cancel)
        self.__confirm.show()

    def show_dialog(self, dialog: 'Dialog') -> None:
        self.__window.addOverlay(dialog)

class Dialog(QWidget, BaseView):
    __on_close_fn: callable = None
    __on_show_fn: callable = None

    def __init__(self):
        super().__init__()
        self.__init_ui()
        self.apply_light_mode()

    def __init_ui(self):
        self.setContentsMargins(24, 24, 24, 16)
        self.__background = QWidget(self)

        self.__btn_close = IconButton.build(
            padding=Paddings.RELATIVE_50,
            size=Icons.MEDIUM,
            style=IconButtonStyle(
                light_mode_icon=Icons.CLOSE.with_color(Colors.GRAY),
                light_mode_background=Backgrounds.ROUNDED_HIDDEN_GRAY_25
            ),
            parent=self
        )
        self.__btn_close.clicked.connect(lambda: self.__on_close_fn())
        self._build_content()

    @abstractmethod
    def _build_content(self) -> None:
        pass

    @override
    def show(self) -> None:
        super().show()
        self.__on_show_fn()

    @override
    def resizeEvent(self, event: QResizeEvent) -> None:
        self.__background.resize(self.size())
        self.__btn_close.move(self.size().width() - self.__btn_close.width() - 4, 4)

    @override
    def apply_dark_mode(self) -> None:
        self.__background.setStyleSheet(Backgrounds.ROUNDED_BLACK.with_border_radius(12).to_stylesheet())
        self.__btn_close.apply_dark_mode()

    @override
    def apply_light_mode(self) -> None:
        self.__background.setStyleSheet(Backgrounds.ROUNDED_WHITE.with_border_radius(12).to_stylesheet())
        self.__btn_close.apply_light_mode()

    @connector
    def on_show(self, fn: callable) -> None:
        self.__on_show_fn = fn

    @connector
    def on_close(self, fn: callable) -> None:
        self.__on_close_fn = fn

    def _on_accepted(self) -> None:
        self.hide()
        if self.__on_close_fn is not None:
            self.__on_close_fn()

    def _on_cancel(self) -> None:
        self.hide()
        if self.__on_close_fn is not None:
            self.__on_close_fn()



class AlertDialog(QWidget, BaseView):
    _onclick_accept_fn: Callable[[], bool]
    __on_show_fn: callable

    def __init__(self, dark_mode: bool = False, ):
        super().__init__()
        self.__init_ui()
        if dark_mode:
            self.apply_dark_mode()
        else:
            self.apply_light_mode()
        self.hide()

    def __init_ui(self):
        self.setContentsMargins(24, 24, 24, 16)
        self.__background = QWidget(self)

        self.__image = Cover()
        self.__image.setAlignment(Qt.AlignHCenter)

        self.__header = LabelWithDefaultText.build(
            font=FontBuilder.build(family="Segoe UI Semibold", size=16, bold=True),
            light_mode_style=TextStyle(text_color=ColorBoxes.BLACK),
            dark_mode_style=TextStyle(text_color=ColorBoxes.WHITE),
        )
        self.__header.setAlignment(Qt.AlignCenter)

        self.__message = LabelWithDefaultText.build(
            font=FontBuilder.build(size=11),
            light_mode_style=TextStyle(text_color=ColorBoxes.BLACK),
            dark_mode_style=TextStyle(text_color=ColorBoxes.WHITE),
        )
        self.__message.setAlignment(Qt.AlignCenter)

        self.__button_box = QHBoxLayout()

        self.__accept_btn = ActionButton.build(
            font=FontBuilder.build(size=12, family="Segoe UI Semibold"),
            size=QSize(0, 48),
            light_mode=TextStyle(text_color=ColorBoxes.WHITE,
                                 background=Backgrounds.ROUNDED_PRIMARY_75.with_border_radius(8)),
            dark_mode=TextStyle(text_color=ColorBoxes.WHITE, background=Backgrounds.ROUNDED_WHITE_25)
        )
        self.__accept_btn.clicked.connect(lambda: self._on_accepted())
        self.__button_box.addWidget(self.__accept_btn)

        self.__view_layout = QVBoxLayout(self)
        self.__view_layout.setAlignment(Qt.AlignVCenter)
        self.__view_layout.setSpacing(12)

        self.__view_layout.addWidget(self.__image)
        self.__view_layout.addWidget(self.__header)
        self.__view_layout.addWidget(self.__message)
        self.__view_layout.addLayout(self.__button_box)
        self.setFixedWidth(360)

    def set_info(self, image: bytes, header: str, message: str, accept_text: str) -> None:
        self.__image.set_cover(CoverProp.from_bytes(image, width=128))
        self.__header.setText(header)
        self.__message.setText(message)
        self.__accept_btn.setText(accept_text)
        self.setMaximumHeight(self.sizeHint().height())

    @override
    def show(self) -> None:
        super().show()
        self.__on_show_fn()

    @override
    def resizeEvent(self, event: QResizeEvent) -> None:
        self.__background.resize(self.size())

    def _get_onclick_accept_fn(self) -> Callable[[], bool]:
        return self._onclick_accept_fn

    def _on_accepted(self) -> None:
        self.hide()
        fn = self._get_onclick_accept_fn()
        if fn is not None:
            fn()

    @override
    def apply_dark_mode(self) -> None:
        self.__background.setStyleSheet(Backgrounds.ROUNDED_BLACK.with_border_radius(12).to_stylesheet())
        self.__header.apply_dark_mode()
        self.__message.apply_dark_mode()
        self.__accept_btn.apply_dark_mode()

    @override
    def apply_light_mode(self) -> None:
        self.__background.setStyleSheet(Backgrounds.ROUNDED_WHITE.with_border_radius(12).to_stylesheet())
        self.__header.apply_light_mode()
        self.__message.apply_light_mode()
        self.__accept_btn.apply_light_mode()

    def on_close(self, fn: callable) -> None:
        self._onclick_accept_fn = fn

    def on_show(self, fn: callable) -> None:
        self.__on_show_fn = fn


class ConfirmDialog(QWidget, BaseView):
    __on_close_fn: callable = None
    __on_show_fn: callable = None
    __on_accept_fn: callable = None
    __on_cancel_fn: callable = None

    def __init__(self):
        super().__init__()
        self.__init_ui()
        self.apply_light_mode()
        self.hide()

    def __init_ui(self):
        self.setContentsMargins(24, 24, 24, 16)
        self.__background = QWidget(self)

        self.__image = Cover()
        self.__image.setAlignment(Qt.AlignHCenter)

        self.__header = LabelWithDefaultText.build(
            font=FontBuilder.build(family="Segoe UI Semibold", size=16, bold=True),
            light_mode_style=TextStyle(text_color=ColorBoxes.BLACK),
            dark_mode_style=TextStyle(text_color=ColorBoxes.WHITE),
        )
        self.__header.setAlignment(Qt.AlignCenter)

        self.__message = LabelWithDefaultText.build(
            font=FontBuilder.build(size=11),
            light_mode_style=TextStyle(text_color=ColorBoxes.BLACK),
            dark_mode_style=TextStyle(text_color=ColorBoxes.WHITE),
        )
        self.__message.setAlignment(Qt.AlignCenter)
        self.__message.setContentsMargins(0, 0, 0, 12)

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
        self.__accept_btn.clicked.connect(lambda: self._on_accepted())
        self.__button_box.addWidget(self.__accept_btn)

        self.__view_layout = QVBoxLayout(self)
        self.__view_layout.setAlignment(Qt.AlignVCenter)
        self.__view_layout.addWidget(self.__image)
        self.__view_layout.addWidget(self.__header)
        self.__view_layout.addWidget(self.__message)
        self.__view_layout.addLayout(self.__button_box)
        self.setFixedWidth(360)

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
    def show(self) -> None:
        super().show()
        self.__on_show_fn()

    @override
    def resizeEvent(self, event: QResizeEvent) -> None:
        self.__background.resize(self.size())

    @override
    def apply_dark_mode(self) -> None:
        self.__background.setStyleSheet(Backgrounds.ROUNDED_BLACK.with_border_radius(12).to_stylesheet())
        self.__header.apply_dark_mode()
        self.__message.apply_dark_mode()
        self.__cancel_btn.apply_dark_mode()
        self.__accept_btn.apply_dark_mode()

    @override
    def apply_light_mode(self) -> None:
        self.__background.setStyleSheet(Backgrounds.ROUNDED_WHITE.with_border_radius(12).to_stylesheet())
        self.__header.apply_light_mode()
        self.__message.apply_light_mode()
        self.__cancel_btn.apply_light_mode()
        self.__accept_btn.apply_light_mode()

    @connector
    def on_accept(self, fn: callable) -> None:
        self.__on_accept_fn = fn

    @connector
    def on_cancel(self, fn: callable) -> None:
        self.__on_cancel_fn = fn

    @connector
    def on_close(self, fn: callable) -> None:
        self.__on_close_fn = fn

    @connector
    def on_show(self, fn: callable) -> None:
        self.__on_show_fn = fn

    def _on_accepted(self) -> None:
        self.hide()
        if self.__on_close_fn is not None:
            self.__on_close_fn()
        if self.__on_accept_fn is not None:
            self.__on_accept_fn()

    def _on_cancel(self) -> None:
        self.hide()
        if self.__on_close_fn is not None:
            self.__on_close_fn()
        if self.__on_cancel_fn is not None:
            self.__on_cancel_fn()


