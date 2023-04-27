from typing import Optional, Callable

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QWidget, QHBoxLayout

from modules.helpers.types.Decorators import override
from modules.models.view.builder.FontBuilder import FontBuilder
from modules.models.view.builder.TextStyle import TextStyle
from modules.screens.AbstractScreen import BaseView
from modules.statics.view.Material import ColorBoxes, Backgrounds
from modules.widgets.Buttons import ActionButton
from modules.widgets.Labels import LabelWithDefaultText


def confirm(
    header: str,
    msg: str,
    accept_text: str = "Confirm",
    reject_text: str = "Cancel",
    onclick_accept_fn: callable = None,
    onclick_reject_fn: callable = None,
    dark_mode: bool = False,
):
    ConfirmDialog(header, msg, accept_text, reject_text, onclick_accept_fn, onclick_reject_fn, dark_mode).exec()


class ConfirmDialog(QDialog, BaseView):
    _onclick_accept_fn: Callable[[], bool]
    _onclick_reject_fn: Callable[[], bool]

    def __init__(
        self,
        header: str,
        msg: str | None = None,
        accept_text: str = "Confirm",
        reject_text: str = "Cancel",
        onclick_accept_fn: Callable[[], bool] = None,
        onclick_reject_fn: Callable[[], bool] = None,
        dark_mode: bool = False,
        parent: Optional["QWidget"] = None,
    ):
        self._onclick_accept_fn = onclick_accept_fn
        self._onclick_reject_fn = onclick_reject_fn
        super().__init__(parent)
        self.__init_ui(header, msg, accept_text, reject_text)
        if dark_mode:
            self.apply_dark_mode()
        else:
            self.apply_light_mode()

    def __init_ui(
        self,
        header: str,
        msg: str,
        accept_text: str,
        reject_text: str,
    ):
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowMinMaxButtonsHint)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.__view = QWidget(self)
        self.__view.setContentsMargins(24, 24, 24, 16)

        content = QWidget()
        self._init_content(content)
        self.__button_box = QHBoxLayout()

        self.__accept_btn = ActionButton.build(
            font=FontBuilder.build(size=10, bold=True),
            size=QSize(144, 48),
            light_mode=TextStyle(text_color=ColorBoxes.WHITE,
                                 background=Backgrounds.ROUNDED_PRIMARY_75.with_border_radius(8)),
            dark_mode=TextStyle(text_color=ColorBoxes.WHITE, background=Backgrounds.ROUNDED_WHITE_25)
        )
        self.__accept_btn.setText(accept_text)
        self.__accept_btn.clicked.connect(lambda: self._on_accepted())
        self.__button_box.addWidget(self.__accept_btn)

        self.__reject_btn = ActionButton.build(
            size=QSize(144, 48),
            font=FontBuilder.build(size=10, bold=True),
            light_mode=TextStyle(text_color=ColorBoxes.WHITE,
                                 background=Backgrounds.ROUNDED_DANGER_75.with_border_radius(8)),
            dark_mode=TextStyle(text_color=ColorBoxes.WHITE, background=Backgrounds.ROUNDED_WHITE_25)
        )
        self.__reject_btn.clicked.connect(lambda: self._on_rejected())
        self.__reject_btn.setText(reject_text)
        self.__button_box.addWidget(self.__reject_btn)

        self.__header = LabelWithDefaultText.build(
            font=FontBuilder.build(size=16, bold=True),
            light_mode_style=TextStyle(text_color=ColorBoxes.BLACK),
            dark_mode_style=TextStyle(text_color=ColorBoxes.WHITE),
        )
        self.__header.setText(header)

        self.__message = LabelWithDefaultText.build(
            font=FontBuilder.build(size=10),
            light_mode_style=TextStyle(text_color=ColorBoxes.BLACK),
            dark_mode_style=TextStyle(text_color=ColorBoxes.WHITE),
        )
        if msg is None or msg == "":
            self.__message.hide()
        self.__message.setText(msg)

        self.__view_layout = QVBoxLayout(self.__view)
        self.__view_layout.setSpacing(20)
        self.__view_layout.addWidget(self.__header)
        self.__view_layout.addWidget(self.__message)
        self.__view_layout.addWidget(content)
        self.__view_layout.addLayout(self.__button_box)
        self.__view.setFixedSize(self.__view.sizeHint())

    def _init_content(self, content: QWidget) -> None:
        pass

    def _get_onclick_accept_fn(self) -> Callable[[], bool]:
        return self._onclick_accept_fn

    def _get_onclick_reject_fn(self) -> Callable[[], bool]:
        return self._onclick_reject_fn

    def _on_accepted(self) -> None:
        fn = self._get_onclick_accept_fn()
        if fn is None:
            self.accept()
            return
        can_close = fn()
        if can_close:
            self.accept()

    def _on_rejected(self) -> None:
        fn = self._get_onclick_reject_fn()
        if fn is not None:
            fn()
        self.reject()

    @override
    def apply_dark_mode(self) -> None:
        self.__view.setStyleSheet(Backgrounds.ROUNDED_BLACK.with_border_radius(24).to_stylesheet())
        self.__header.apply_dark_mode()
        self.__message.apply_dark_mode()
        self.__accept_btn.apply_dark_mode()
        self.__reject_btn.apply_dark_mode()

    @override
    def apply_light_mode(self) -> None:
        self.__view.setStyleSheet(Backgrounds.ROUNDED_WHITE.with_border_radius(24).to_stylesheet())
        self.__header.apply_light_mode()
        self.__message.apply_light_mode()
        self.__accept_btn.apply_light_mode()
        self.__reject_btn.apply_light_mode()
