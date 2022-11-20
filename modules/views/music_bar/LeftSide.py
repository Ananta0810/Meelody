from typing import Optional, Union

from PyQt5.QtCore import QMetaObject
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QHBoxLayout, QWidget, QVBoxLayout

from modules.helpers.PixmapHelper import PixmapHelper
from modules.models.view.builder.FontBuilder import FontBuilder
from modules.models.view.builder.IconButtonStyle import IconButtonStyle
from modules.models.view.builder.TextStyle import TextStyle
from modules.statics.view.Material import Paddings, Icons, Colors, Backgrounds, ColorBoxes
from modules.widgets.IconButton import IconButton
from modules.widgets.ImageViewer import ImageViewer
from modules.widgets.LabelWithDefaultText import LabelWithDefaultText
from modules.widgets.StatelessIconButton import StatelessIconButton


class MusicPlayerLeftSide(QHBoxLayout):
    song_info_layout: QVBoxLayout
    play_buttons: QHBoxLayout

    song_cover: ImageViewer
    song_artist: LabelWithDefaultText
    song_title: LabelWithDefaultText

    prev_song_btn: IconButton
    play_song_btn: StatelessIconButton
    next_song_btn: IconButton

    def __init__(self, parent: Optional["QWidget"] = None):
        super(MusicPlayerLeftSide, self).__init__(parent)
        self.setup_ui()

    def setup_ui(self) -> None:
        self.song_cover = ImageViewer()
        self.song_cover.setFixedSize(64, 64)
        self.addWidget(self.song_cover)

        self.song_title = LabelWithDefaultText.build(
            width=128,
            font=FontBuilder.build(size=10, bold=True),
            light_mode_style=TextStyle(text_color=ColorBoxes.BLACK),
            dark_mode_style=TextStyle(text_color=ColorBoxes.WHITE)
        )
        self.song_artist = LabelWithDefaultText.build(
            width=128,
            font=FontBuilder.build(size=9),
            light_mode_style=TextStyle(text_color=ColorBoxes.BLACK),
            dark_mode_style=TextStyle(text_color=ColorBoxes.WHITE)
        )

        self.song_info_layout = QVBoxLayout()
        self.song_info_layout.setContentsMargins(0, 0, 0, 0)
        self.song_info_layout.setSpacing(0)
        self.addLayout(self.song_info_layout, stretch=1)
        self.song_info_layout.addStretch(0)
        self.song_info_layout.addWidget(self.song_title)
        self.song_info_layout.addWidget(self.song_artist)
        self.song_info_layout.addStretch(0)

        # =================PREVIOUS - PLAY - NEXT=================
        self.play_buttons = QHBoxLayout()
        self.play_buttons.setContentsMargins(0, 0, 0, 0)
        self.play_buttons.setSpacing(8)
        self.addLayout(self.play_buttons)

        self.prev_song_btn = IconButton.build(
            padding=Paddings.RELATIVE_50,
            size=Icons.LARGE,
            style=IconButtonStyle(
                light_mode_icon=Icons.PREVIOUS.with_color(Colors.PRIMARY),
                light_mode_background=Backgrounds.CIRCLE_HIDDEN_PRIMARY_25,
            )
        )
        self.play_buttons.addWidget(self.prev_song_btn)

        self.play_song_btn = StatelessIconButton.build(
            padding=Paddings.RELATIVE_50,
            size=Icons.X_LARGE,
            children=[
                IconButtonStyle(
                    light_mode_icon=Icons.PLAY.with_color(Colors.PRIMARY),
                    dark_mode_icon=Icons.PLAY.with_color(Colors.WHITE),
                    light_mode_background=Backgrounds.CIRCLE_PRIMARY_25,
                    dark_mode_background=Backgrounds.CIRCLE_PRIMARY,
                ),
                IconButtonStyle(
                    light_mode_icon=Icons.PAUSE.with_color(Colors.PRIMARY),
                    dark_mode_icon=Icons.PAUSE.with_color(Colors.WHITE),
                    light_mode_background=Backgrounds.CIRCLE_PRIMARY_25,
                    dark_mode_background=Backgrounds.CIRCLE_PRIMARY,
                ),
            ],
        )
        self.play_song_btn.setChecked(False)
        self.play_buttons.addWidget(self.play_song_btn)

        self.next_song_btn = IconButton.build(
            padding=Paddings.RELATIVE_50,
            size=Icons.LARGE,
            style=IconButtonStyle(
                light_mode_icon=Icons.NEXT.with_color(Colors.PRIMARY),
                light_mode_background=Backgrounds.CIRCLE_HIDDEN_PRIMARY_25,
            )
        )
        self.play_buttons.addWidget(self.next_song_btn)
        QMetaObject.connectSlotsByName(self)

    def apply_light_mode(self) -> None:
        self.next_song_btn.apply_light_mode()
        self.prev_song_btn.apply_light_mode()
        self.play_song_btn.apply_light_mode()
        self.song_title.apply_light_mode()
        self.song_artist.apply_light_mode()

    def apply_dark_mode(self) -> None:
        self.next_song_btn.apply_dark_mode()
        self.prev_song_btn.apply_dark_mode()
        self.play_song_btn.apply_dark_mode()
        self.song_title.apply_dark_mode()
        self.song_artist.apply_dark_mode()

    def set_default_cover(self, byte_pixmap: bytes) -> None:
        self.song_cover.set_default_pixmap(self.__get_pixmap_for_song_cover(byte_pixmap))

    def set_default_title(self, text: str) -> None:
        self.song_title.set_default_text(text)

    def set_default_artist(self, text: str) -> None:
        self.song_artist.set_default_text(text)

    def set_cover(self, byte_pixmap: bytes) -> None:
        self.song_cover.set_pixmap(self.__get_pixmap_for_song_cover(byte_pixmap))

    def set_title(self, text: str) -> None:
        self.song_title.set_text(text)

    def set_artist(self, text: str) -> None:
        self.song_artist.set_text(text)

    @staticmethod
    def __get_pixmap_for_song_cover(byte_pixmap: bytes) -> Union[QPixmap, None]:
        if byte_pixmap is None:
            return None
        pixmap = PixmapHelper.get_rounded_squared_pixmap_from_bytes(byte_pixmap, edge=64, radius=12)
        return pixmap
