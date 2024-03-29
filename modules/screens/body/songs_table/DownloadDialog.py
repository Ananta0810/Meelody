from typing import Callable

from PyQt5.QtCore import QSize, Qt, pyqtSignal
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QShortcut

from modules.helpers.types.Decorators import override, connector
from modules.models.view.Background import Background
from modules.models.view.Border import Border
from modules.models.view.Color import Color
from modules.models.view.ColorBox import ColorBox
from modules.models.view.builder.FontBuilder import FontBuilder
from modules.models.view.builder.TextStyle import TextStyle
from modules.screens.AbstractScreen import BaseView
from modules.screens.body.songs_table.DownloadMenu import DownloadMenu
from modules.statics.view.Material import ColorBoxes, Backgrounds, Colors, Images
from modules.widgets import Dialogs
from modules.widgets.Buttons import ActionButton
from modules.widgets.Cover import Cover, CoverProp
from modules.widgets.Labels import LabelWithDefaultText, Input


class DownloadDialog(Dialogs.Dialog, BaseView):
    closed: pyqtSignal() = pyqtSignal()
    __on_accept_fn: callable = None

    @override
    def _build_content(self) -> None:
        self.__image = Cover()
        self.__image.setAlignment(Qt.AlignHCenter)
        self.__header = LabelWithDefaultText.build(
            font=FontBuilder.build(family="Segoe UI Semibold", size=16, bold=True),
            light_mode_style=TextStyle(text_color=ColorBoxes.BLACK),
            dark_mode_style=TextStyle(text_color=ColorBoxes.WHITE),
        )
        self.__header.setAlignment(Qt.AlignCenter)

        self.__input = Input.build(
            font=FontBuilder.build(size=12),
            light_mode_style=TextStyle(
                text_color=ColorBoxes.BLACK,
                background=(Background(border_radius=8,
                                       color=ColorBox(normal=Colors.GRAY.with_opacity(8)),
                                       border=Border(size=2, color=ColorBox(Color(216, 216, 216)))
                                       ))
            ),
            padding=8
        )
        self.__input.setFixedHeight(48)
        self.__accept_btn = ActionButton.build(
            font=FontBuilder.build(family="Segoe UI Semibold", size=11),
            size=QSize(0, 48),
            light_mode=TextStyle(text_color=ColorBoxes.WHITE,
                                 background=Backgrounds.ROUNDED_PRIMARY_75.with_border_radius(8)),
            dark_mode=TextStyle(text_color=ColorBoxes.WHITE, background=Backgrounds.ROUNDED_WHITE_25)
        )

        self.__menu_outer = QWidget()
        self.__menu_outer.setContentsMargins(24, 12, 24, 24)
        layout = QVBoxLayout(self.__menu_outer)
        layout.setContentsMargins(0, 0, 0, 0)
        self.__menu = DownloadMenu()
        layout.addWidget(self.__menu)

        self.__main_view = QWidget()
        self.__main_view.setContentsMargins(24, 24, 24, 0)

        cover_wrapper_layout = QVBoxLayout()
        self.__image.setFixedHeight(156)
        cover_wrapper_layout.addWidget(self.__image)

        self.__view_layout = QVBoxLayout(self.__main_view)
        self.__view_layout.setContentsMargins(0, 0, 0, 0)
        self.__view_layout.setAlignment(Qt.AlignVCenter)
        self.__view_layout.addLayout(cover_wrapper_layout)
        self.__view_layout.addWidget(self.__header)
        self.__view_layout.addSpacing(4)
        self.__view_layout.addWidget(self.__input)
        self.__view_layout.addSpacing(8)
        self.__view_layout.addWidget(self.__accept_btn)

        self.addWidget(self.__main_view)
        self.addWidget(self.__menu_outer)

        self.__image.set_cover(CoverProp.from_bytes(Images.DOWNLOAD, width=128))
        self.__header.setText("Download Youtube Song")
        self.__accept_btn.setText("Download")

        self.setFixedWidth(640)
        self.setFixedHeight(self.__height())

    @override
    def connectToSignalSlot(self):
        super().connectToSignalSlot()
        self.__accept_btn.clicked.connect(lambda: self._on_accepted())

    @override
    def assignShortcuts(self) -> None:
        super().assignShortcuts()
        acceptShortcut = QShortcut(QKeySequence(Qt.Key_Return), self.__accept_btn)
        acceptShortcut.activated.connect(self.__accept_btn.click)

    @override
    def close(self) -> bool:
        self.closed.emit()
        return super().close()

    @override
    def apply_dark_mode(self) -> None:
        super().apply_dark_mode()
        self.__header.apply_dark_mode()
        self.__input.apply_dark_mode()
        self.__accept_btn.apply_dark_mode()
        self.__menu.apply_dark_mode()

    @override
    def apply_light_mode(self) -> None:
        super().apply_light_mode()
        self.__header.apply_light_mode()
        self.__input.apply_light_mode()
        self.__accept_btn.apply_light_mode()
        self.__menu.apply_light_mode()

    @override
    def show(self) -> None:
        super().show()
        self.__input.clear()

    @connector
    def on_download(self, fn: Callable[[str], None]) -> None:
        self.__on_accept_fn = fn

    def _on_accepted(self) -> None:
        if self.__on_accept_fn is not None:
            self.__on_accept_fn(self.__input.text())

    def add_item(self, label: str) -> None:
        self.__menu.add(label)
        self.setFixedHeight(self.__height())

    def __height(self):
        return self.__main_view.sizeHint().height() + self.__menu_outer.sizeHint().height()

    def mark_succeed_at(self, index: int) -> None:
        self.__menu.mark_succeed_at(index)

    def mark_processing_at(self, index: int) -> None:
        self.__menu.mark_processing_at(index)

    def mark_failed_at(self, index: int) -> None:
        self.__menu.mark_failed_at(index)

    def set_description_at(self, index: int, value: str) -> None:
        self.__menu.set_description_at(index, value)

    def set_progress_at(self, index: int, value: float) -> None:
        self.__menu.set_progress_at(index, value)
