from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QHBoxLayout

from modules.helpers.types.Decorators import override
from modules.models.view.AppIcon import AppIcon
from modules.models.view.Padding import Padding
from modules.models.view.builder.FontBuilder import FontBuilder
from modules.models.view.builder.IconButtonStyle import IconButtonStyle
from modules.models.view.builder.TextStyle import TextStyle
from modules.statics.view.Material import ColorBoxes, Icons, Paddings, Colors, Backgrounds
from modules.views.ViewComponent import ViewComponent
from modules.widgets.IconButton import IconButton
from modules.widgets.LabelWithDefaultText import LabelWithDefaultText


class SongTableHeader(QWidget, ViewComponent):
    __main_layout: QHBoxLayout
    __info: QHBoxLayout

    __label_track: LabelWithDefaultText
    __label_artist: LabelWithDefaultText
    __label_length: LabelWithDefaultText

    __buttons: QWidget
    __buttons_layout: QHBoxLayout
    __btn_download_songs: IconButton
    __btn_add_songs: IconButton

    def __init__(self, parent: Optional["QWidget"] = None):
        super(SongTableHeader, self).__init__(parent)
        self.__init_ui()

    def __init_ui(self) -> None:
        SCROLLBAR_WIDTH = 4
        font = FontBuilder.build(size=9)

        self.setAttribute(Qt.WA_StyledBackground, True)

        self.__main_layout = QHBoxLayout(self)
        self.__main_layout.setContentsMargins(28, 0, 28 + SCROLLBAR_WIDTH, 0)
        self.__main_layout.setSpacing(0)

        self.__info = QHBoxLayout()
        self.__info.setContentsMargins(0, 0, 0, 0)
        self.__info.setSpacing(24)

        self.__main_layout.addLayout(self.__info)

        self.__label_track = self.__create_label(font)
        self.__label_track.setFixedWidth(64)
        self.__label_track.setAlignment(Qt.AlignCenter)

        self.__label_artist = self.__create_label(font)
        self.__label_artist.setFixedWidth(128)

        self.__label_length = self.__create_label(font)
        self.__label_length.setFixedWidth(64)
        self.__label_length.setAlignment(Qt.AlignCenter)

        self.__buttons = QWidget()
        self.__buttons_layout = QHBoxLayout(self.__buttons)
        self.__buttons_layout.setAlignment(Qt.AlignRight)
        self.__buttons_layout.setSpacing(8)
        self.__buttons_layout.setContentsMargins(8, 0, 8, 0)

        self.__buttons_layout.addSpacing(48)
        self.__buttons_layout.addSpacing(8)

        self.__btn_download_songs = self.__create_button(Icons.DOWNLOAD, Paddings.RELATIVE_50)
        self.__btn_add_songs = self.__create_button(Icons.ADD, Paddings.RELATIVE_75)

        self.__buttons_layout.addWidget(self.__btn_download_songs)
        self.__buttons_layout.addWidget(self.__btn_add_songs)

        self.__info.addWidget(self.__label_track)
        self.__info.addStretch(1)
        self.__info.addSpacing(24)
        self.__info.addWidget(self.__label_artist, 1)
        self.__info.addWidget(self.__label_length)
        self.__info.addWidget(self.__buttons)

    @override
    def apply_light_mode(self) -> None:
        self.__label_track.apply_light_mode()
        self.__label_artist.apply_light_mode()
        self.__label_length.apply_light_mode()
        self.__btn_download_songs.apply_light_mode()
        self.__btn_add_songs.apply_light_mode()

    @override
    def apply_dark_mode(self) -> None:
        self.__label_track.apply_dark_mode()
        self.__label_artist.apply_dark_mode()
        self.__label_length.apply_dark_mode()
        self.__btn_download_songs.apply_dark_mode()
        self.__btn_add_songs.apply_dark_mode()

    @override
    def setText(self, track: str = "TRACK", artist: str = "ARTIST", length: str = "LENGTH") -> None:
        self.__label_track.setText(track)
        self.__label_artist.setText(artist)
        self.__label_length.setText(length)

    @staticmethod
    def __create_label(font: QFont) -> LabelWithDefaultText:
        return LabelWithDefaultText.build(
            font,
            light_mode_style=TextStyle(text_color=ColorBoxes.BLACK),
            dark_mode_style=TextStyle(text_color=ColorBoxes.WHITE)
        )

    @staticmethod
    def __create_button(icon: AppIcon, padding: Padding) -> IconButton:
        return IconButton.build(
            size=Icons.LARGE,
            padding=padding,
            style=IconButtonStyle(
                light_mode_icon=icon.with_color(Colors.PRIMARY),
                dark_mode_icon=icon.with_color(Colors.WHITE),
                light_mode_background=Backgrounds.CIRCLE_PRIMARY_10,
                dark_mode_background=Backgrounds.CIRCLE_WHITE_25,
            )
        )