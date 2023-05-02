from typing import Optional

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QResizeEvent, QMovie
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QSizePolicy, QGridLayout, QLabel

from modules.helpers.types.Decorators import override
from modules.models.view.builder.BackgroundThemeBuilder import BackgroundThemeBuilder
from modules.models.view.builder.FontBuilder import FontBuilder
from modules.models.view.builder.IconButtonStyle import IconButtonStyle
from modules.models.view.builder.TextStyle import TextStyle
from modules.screens.AbstractScreen import BaseView
from modules.statics.view.Material import Images, Backgrounds, ColorBoxes, Icons, Paddings, Colors, Cursors
from modules.widgets.Buttons import IconButton, StatelessIconButton
from modules.widgets.Cover import CoverProp, Cover
from modules.widgets.Labels import LabelWithDefaultText
from modules.widgets.ProgressBars import ProgressBar
from modules.widgets.ScrollAreas import SmoothVerticalScrollArea
from modules.widgets.Widgets import BackgroundWidget

_downloading = 1
_processing = 2
_finished = 3


class DownloadRow(BackgroundWidget, BaseView):

    def __init__(self, parent: Optional["QWidget"] = None):
        super().__init__(parent)
        self.__init_ui()
        self.__state = _downloading
        self.__gif_movie: QMovie | None = None
        self.__dot: float = 0
        self.__frame: int = 0
        self.__cover.set_cover(CoverProp.from_bytes(Images.DEFAULT_SONG_COVER, width=48, height=48, radius=8))
        self.set_progress(0)

    def __init_ui(self) -> None:
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

        self.__progress_bar = ProgressBar()
        self.__progress_bar.setFixedHeight(2)
        self.__progress_bar.set_progress_style(Backgrounds.CIRCLE_PRIMARY.with_border_radius(1))

        info_layout = QVBoxLayout()
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(4)
        info_layout.addStretch(0)
        info_layout.addWidget(self.__label_title)
        info_layout.addWidget(self.__label_description)
        info_layout.addWidget(self.__progress_bar)
        info_layout.addStretch(0)

        icons = QWidget()
        icons.setFixedWidth(48)

        self.__result_icon = StatelessIconButton.build(
            size=Icons.SMALL,
            padding=Paddings.RELATIVE_25,
            children=[
                IconButtonStyle(
                    light_mode_icon=Icons.APPLY.with_color(Colors.WHITE),
                    light_mode_background=Backgrounds.CIRCLE_PRIMARY,
                ),
                IconButtonStyle(
                    light_mode_icon=Icons.CLOSE.with_color(Colors.WHITE),
                    light_mode_background=Backgrounds.CIRCLE_DANGER,
                )
            ],
        )
        self.__result_icon.keep_space_when_hiding()
        self.__result_icon.setCursor(Cursors.DEFAULT)
        self.__result_icon.hide()

        self.__gif = QLabel()
        self.__gif.setFixedSize(48, 48)

        self.__icons_layout = QVBoxLayout(icons)
        self.__icons_layout.addWidget(self.__gif)
        self.__icons_layout.addWidget(self.__result_icon)

        self.__main_layout = QHBoxLayout()
        self.__main_layout.setSpacing(0)
        self.__main_layout.setSpacing(0)
        self.__main_layout.setAlignment(Qt.AlignLeft)

        self.__main_layout.addWidget(self.__cover)
        self.__main_layout.addSpacing(12)
        self.__main_layout.addLayout(info_layout, stretch=1)
        self.__main_layout.addWidget(icons)

        self.setLayout(self.__main_layout)

    @override
    def resizeEvent(self, a0: QResizeEvent) -> None:
        super().resizeEvent(a0)
        self.__label_title.setFixedWidth(self.__progress_bar.sizeHint().width())

    @override
    def apply_light_mode(self) -> None:
        self.__label_title.apply_light_mode()
        self.__label_description.apply_light_mode()
        self.__progress_bar.apply_light_mode()
        self.__result_icon.apply_light_mode()

    @override
    def apply_dark_mode(self) -> None:
        self.__label_title.apply_dark_mode()
        self.__label_description.apply_dark_mode()
        self.__progress_bar.apply_dark_mode()
        self.__result_icon.apply_dark_mode()

    def mark_succeed(self) -> None:
        self.__state = _finished
        self.__result_icon.show()
        self.__result_icon.set_state_index(0)
        self.__gif.setFixedSize(0, 0)
        self.__icons_layout.addSpacing(24)
        if self.__gif_movie is not None:
            self.__gif_movie.stop()
            self.__gif_movie = None
        self.__label_description.setText("Download Succeed.")

    def mark_failed(self) -> None:
        self.__state = _finished
        self.__result_icon.show()
        self.__result_icon.set_state_index(1)
        self.__gif.setFixedSize(0, 0)
        self.__icons_layout.addSpacing(24)
        if self.__gif_movie is not None:
            self.__gif_movie.stop()
            self.__gif_movie = None
        self.__label_description.setText("Download Failed.")

    def mark_processing(self) -> None:
        if self.__state == _finished:
            return

        if self.__state == _downloading:
            self.__state = _processing

        self.set_progress(100)
        self.__label_description.setText(f"Extracting{int(self.__dot) * '.'}")
        self.__dot = (self.__dot + 0.25) % 4

        if self.__gif_movie is None:
            self.__gif_movie = QMovie("assets\images\defaults\loading.gif")
            count = self.__gif_movie.frameCount()
            self.__gif_movie.setScaledSize(self.__gif.size())
            self.__gif.setMovie(self.__gif_movie)
        else:
            self.__gif_movie.jumpToFrame(self.__frame)
            self.__frame = (self.__frame + 1) % self.__gif_movie.frameCount()

    @override
    def resizeEvent(self, a0: QResizeEvent) -> None:
        super().resizeEvent(a0)

    def set_label(self, label: str) -> None:
        self.__label_title.setText(label)

    def set_description(self, value: str) -> None:
        self.__label_description.setText(value)

    def set_progress(self, value: float) -> None:
        self.__progress_bar.set_value(value)
