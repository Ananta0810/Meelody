from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QHBoxLayout

from modules.models.view.AppIcon import AppIcon
from modules.models.view.Padding import Padding
from modules.models.view.builder.FontBuilder import FontBuilder
from modules.models.view.builder.IconButtonStyle import IconButtonStyle
from modules.models.view.builder.TextStyle import TextStyle
from modules.statics.view.Material import ColorBoxes, Icons, Paddings, Colors, Backgrounds
from modules.widgets.IconButton import IconButton
from modules.widgets.LabelWithDefaultText import LabelWithDefaultText


class SongTableHeader(QWidget):
    main_layout: QHBoxLayout
    info: QHBoxLayout

    label_track: LabelWithDefaultText
    label_artist: LabelWithDefaultText
    label_length: LabelWithDefaultText

    buttons: QWidget
    buttons_layout: QHBoxLayout
    btn_download_songs: IconButton
    btn_add_songs: IconButton

    def __init__(self, parent: Optional["QWidget"] = None):
        super(SongTableHeader, self).__init__(parent)
        self.setup_ui()

    def setup_ui(self) -> None:
        SCROLLBAR_WIDTH = 4
        font = FontBuilder.build(size=9)

        self.setAttribute(Qt.WA_StyledBackground, True)

        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(28, 0, 28 + SCROLLBAR_WIDTH, 0)
        self.main_layout.setSpacing(0)

        self.info = QHBoxLayout()
        self.info.setContentsMargins(0, 0, 0, 0)
        self.info.setSpacing(24)

        self.main_layout.addLayout(self.info)

        self.label_track = self.create_label(font)
        self.label_track.setFixedWidth(64)
        self.label_track.setAlignment(Qt.AlignCenter)

        self.label_artist = self.create_label(font)
        self.label_artist.setFixedWidth(128)

        self.label_length = self.create_label(font)
        self.label_length.setFixedWidth(64)
        self.label_length.setAlignment(Qt.AlignCenter)

        self.buttons = QWidget()
        self.buttons_layout = QHBoxLayout(self.buttons)
        self.buttons_layout.setAlignment(Qt.AlignRight)
        self.buttons_layout.setSpacing(8)
        self.buttons_layout.setContentsMargins(8, 0, 8, 0)

        self.buttons_layout.addSpacing(48)
        self.buttons_layout.addSpacing(8)

        self.btn_download_songs = self.create_button(Icons.DOWNLOAD, Paddings.RELATIVE_50)
        self.btn_add_songs = self.create_button(Icons.ADD, Paddings.RELATIVE_75)

        self.buttons_layout.addWidget(self.btn_download_songs)
        self.buttons_layout.addWidget(self.btn_add_songs)

        self.info.addWidget(self.label_track)
        self.info.addStretch(1)
        self.info.addSpacing(24)
        self.info.addWidget(self.label_artist, 1)
        self.info.addWidget(self.label_length)
        self.info.addWidget(self.buttons)

    def apply_light_mode(self) -> None:
        self.label_track.apply_light_mode()
        self.label_artist.apply_light_mode()
        self.label_length.apply_light_mode()
        self.btn_download_songs.apply_light_mode()
        self.btn_add_songs.apply_light_mode()

    def apply_dark_mode(self) -> None:
        self.label_track.apply_dark_mode()
        self.label_artist.apply_dark_mode()
        self.label_length.apply_dark_mode()
        self.btn_download_songs.apply_dark_mode()
        self.btn_add_songs.apply_dark_mode()

    def set_text(self, track="TRACK", artist: str = "ARTIST", length: str = "LENGTH") -> None:
        self.label_track.setText(track)
        self.label_artist.setText(artist)
        self.label_length.setText(length)

    @staticmethod
    def create_label(font: QFont):
        return LabelWithDefaultText.build(
            font,
            light_mode_style=TextStyle(text_color=ColorBoxes.BLACK),
            dark_mode_style=TextStyle(text_color=ColorBoxes.WHITE)
        )

    @staticmethod
    def create_button(icon: AppIcon, padding: Padding) -> IconButton:
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