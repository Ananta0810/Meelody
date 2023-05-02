from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QScrollArea

from modules.helpers.types.Decorators import override
from modules.models.view.builder.BackgroundThemeBuilder import BackgroundThemeBuilder
from modules.models.view.builder.FontBuilder import FontBuilder
from modules.models.view.builder.TextStyle import TextStyle
from modules.screens.AbstractScreen import BaseView
from modules.statics.view.Material import Images, Backgrounds, ColorBoxes
from modules.widgets.Cover import CoverProp, Cover
from modules.widgets.Labels import LabelWithDefaultText
from modules.widgets.ProgressBars import ProgressBar
from modules.widgets.ScrollAreas import SmoothVerticalScrollArea
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
            dark_mode_style=TextStyle(text_color=ColorBoxes.WHITE),
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
        self.__label_title.setFixedWidth(480)

    def set_label(self, label: str) -> None:
        self.__label_title.setText(label)

    def set_description(self, value: str) -> None:
        self.__label_description.setText(value)

    def set_progress(self, value: float) -> None:
        self.__progress_bar.set_value(value)

