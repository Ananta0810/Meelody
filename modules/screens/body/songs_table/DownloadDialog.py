from typing import Callable, Optional

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

from modules.helpers.types.Decorators import override, connector
from modules.models.view.Background import Background
from modules.models.view.Border import Border
from modules.models.view.Color import Color
from modules.models.view.ColorBox import ColorBox
from modules.models.view.builder.BackgroundThemeBuilder import BackgroundThemeBuilder
from modules.models.view.builder.FontBuilder import FontBuilder
from modules.models.view.builder.TextStyle import TextStyle
from modules.screens.AbstractScreen import BaseView
from modules.statics.view.Material import ColorBoxes, Backgrounds, Colors, Images
from modules.widgets.BaseDialogs import Dialog
from modules.widgets.Buttons import ActionButton
from modules.widgets.Cover import Cover, CoverProp
from modules.widgets.Labels import LabelWithDefaultText, Input
from modules.widgets.ProgressBars import ProgressBar
from modules.widgets.Widgets import BackgroundWidget


class DownloadRow(BackgroundWidget, BaseView):

    def __init__(self, parent: Optional["QWidget"] = None):
        super().__init__(parent)
        self.__init_ui()
        self.__cover.set_cover(CoverProp.from_bytes(Images.DEFAULT_SONG_COVER, width=48, height=48, radius=8))
        self.set_progress(0)

    def __init_ui(self) -> None:
        self.__main_layout = QHBoxLayout()
        self.__main_layout.setSpacing(0)
        self.__main_layout.setSpacing(12)
        self.__main_layout.setAlignment(Qt.AlignLeft)
        self.setLayout(self.__main_layout)

        self.__cover = Cover()
        self.__cover.setFixedSize(48, 48)

        self.__label_title = LabelWithDefaultText.build(
            font=FontBuilder.build(size=10, bold=True),
            light_mode_style=TextStyle(text_color=ColorBoxes.BLACK),
            dark_mode_style=TextStyle(text_color=ColorBoxes.WHITE)
        )
        self.__label_description = LabelWithDefaultText.build(
            font=FontBuilder.build(size=9),
            light_mode_style=TextStyle(text_color=ColorBoxes.BLACK),
            dark_mode_style=TextStyle(text_color=ColorBoxes.WHITE)
        )

        info_layout = QVBoxLayout()
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(0)

        info_layout.addStretch(0)
        info_layout.addWidget(self.__label_title)
        info_layout.addWidget(self.__label_description)
        info_layout.addStretch(0)

        self.__main_layout.addWidget(self.__cover)
        self.__main_layout.addLayout(info_layout, stretch=1)

        self.__progress_bar = ProgressBar(self)
        self.__progress_bar.setFixedHeight(2)
        self.__progress_bar.set_progress_style(Backgrounds.CIRCLE_PRIMARY.with_border_radius(1))

    @override
    def apply_light_mode(self) -> None:
        style = BackgroundThemeBuilder.build("QWidget", 12, Backgrounds.CIRCLE_HIDDEN_GRAY_10.with_border_radius(1))
        self.setStyleSheet(style)
        self.__label_title.apply_light_mode()
        self.__label_description.apply_light_mode()
        self.__progress_bar.apply_light_mode()

    @override
    def apply_dark_mode(self) -> None:
        style = BackgroundThemeBuilder.build("QWidget", 12, Backgrounds.CIRCLE_HIDDEN_GRAY_10.with_border_radius(1))
        self.setStyleSheet(style)
        self.__label_title.apply_dark_mode()
        self.__label_description.apply_dark_mode()
        self.__progress_bar.apply_dark_mode()

    @override
    def resizeEvent(self, a0: QResizeEvent) -> None:
        super().resizeEvent(a0)
        self.__progress_bar.setFixedWidth(self.width() - 16)
        self.__progress_bar.move(8, self.height() - self.__progress_bar.height())

    def set_label(self, label: str) -> None:
        self.__label_title.setText(label)

    def set_description(self, value: str) -> None:
        self.__label_description.setText(value)

    def set_progress(self, value: float) -> None:
        self.__progress_bar.set_value(value)


class DownloadDialog(Dialog):
    __on_accept_fn: callable = None

    @override
    def _build_content(self):
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
        self.__accept_btn.clicked.connect(lambda: self._on_accepted())

        self.__download_files = QWidget()
        self.__download_files_layout = QVBoxLayout(self.__download_files)
        self.__download_files_layout.setContentsMargins(0, 0, 0, 0)

        self.__download_sample = DownloadRow()
        self.__download_sample.apply_light_mode()
        self.__download_files_layout.addWidget(self.__download_sample)

        self.__view_layout = QVBoxLayout(self)
        self.__view_layout.setAlignment(Qt.AlignVCenter)
        self.__view_layout.addWidget(self.__image)
        self.__view_layout.addWidget(self.__header)
        self.__view_layout.addSpacing(4)
        self.__view_layout.addWidget(self.__input)
        self.__view_layout.addSpacing(8)
        self.__view_layout.addWidget(self.__accept_btn)
        self.__view_layout.addWidget(self.__download_files)

        self.__image.set_cover(CoverProp.from_bytes(Images.DOWNLOAD, width=128))
        self.__header.setText("Download Youtube Song")
        self.__accept_btn.setText("Download")

        self.setFixedWidth(640)
        self.setFixedHeight(self.sizeHint().height())

    @override
    def apply_dark_mode(self) -> None:
        super().apply_dark_mode()
        self.__header.apply_dark_mode()
        self.__input.apply_dark_mode()
        self.__accept_btn.apply_dark_mode()

    @override
    def apply_light_mode(self) -> None:
        super().apply_light_mode()
        self.__header.apply_light_mode()
        self.__input.apply_light_mode()
        self.__accept_btn.apply_light_mode()

    @connector
    def on_download(self, fn: Callable[[str], None]) -> None:
        self.__on_accept_fn = fn

    def _on_accepted(self) -> None:
        if self.__on_accept_fn is not None:
            self.__on_accept_fn(self.__input.text())

    def set_label_at(self, index: int, label: str) -> None:
        self.__download_sample.set_label(label)

    def set_description_at(self, index: int, value: str) -> None:
        self.__download_sample.set_description(value)

    def set_progress_at(self, index: int, value: float) -> None:
        self.__download_sample.set_progress(value)
