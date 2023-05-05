from typing import Optional, Union

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QHBoxLayout, QWidget, QVBoxLayout, QShortcut

from modules.helpers.types.Decorators import override, connector
from modules.models.view.builder.FontBuilder import FontBuilder
from modules.models.view.builder.IconButtonStyle import IconButtonStyle
from modules.models.view.builder.TextStyle import TextStyle
from modules.screens.AbstractScreen import BaseView
from modules.statics.view.Material import Paddings, Icons, Colors, Backgrounds, ColorBoxes
from modules.widgets.Buttons import IconButton
from modules.widgets.Cover import Cover, CoverProp
from modules.widgets.Labels import LabelWithDefaultText


class MusicPlayerLeftSide(QHBoxLayout, BaseView):
    __song_info_layout: QVBoxLayout = None
    __play_buttons: QHBoxLayout = None

    __song_cover: Cover = None
    __label_song_artist: LabelWithDefaultText = None
    __label_song_title: LabelWithDefaultText = None

    __btn_prev_song: IconButton = None
    __btn_play_song: IconButton = None
    __btn_pause_song: IconButton = None
    __btn_next_song: IconButton = None

    def __init__(self, parent: Optional["QWidget"] = None):
        super().__init__(parent)
        self.__init_ui()
        self.set_is_playing(False)
        self.assign_shortcuts()

    def __init_ui(self) -> None:
        self.__song_cover = Cover()
        self.__song_cover.setFixedSize(64, 64)
        self.addWidget(self.__song_cover)

        self.__label_song_title = LabelWithDefaultText.build(
            width=128,
            font=FontBuilder.build(size=10, bold=True),
            light_mode_style=TextStyle(text_color=ColorBoxes.BLACK),
            dark_mode_style=TextStyle(text_color=ColorBoxes.WHITE)
        )
        self.__label_song_artist = LabelWithDefaultText.build(
            width=128,
            font=FontBuilder.build(size=9),
            light_mode_style=TextStyle(text_color=ColorBoxes.BLACK),
            dark_mode_style=TextStyle(text_color=ColorBoxes.WHITE)
        )

        self.__song_info_layout = QVBoxLayout()
        self.__song_info_layout.setContentsMargins(0, 0, 0, 0)
        self.__song_info_layout.setSpacing(0)

        self.addLayout(self.__song_info_layout, stretch=1)

        self.__song_info_layout.addStretch(0)
        self.__song_info_layout.addWidget(self.__label_song_title)
        self.__song_info_layout.addWidget(self.__label_song_artist)
        self.__song_info_layout.addStretch(0)

        # =================PREVIOUS - PLAY - NEXT=================
        self.__play_buttons = QHBoxLayout()
        self.__play_buttons.setContentsMargins(0, 0, 0, 0)
        self.__play_buttons.setSpacing(8)
        self.addLayout(self.__play_buttons)

        self.__btn_prev_song = IconButton.build(
            padding=Paddings.RELATIVE_50,
            size=Icons.LARGE,
            style=IconButtonStyle(
                light_mode_icon=Icons.PREVIOUS.with_color(Colors.PRIMARY),
                light_mode_background=Backgrounds.CIRCLE_HIDDEN_PRIMARY_10,
            )
        )
        self.__play_buttons.addWidget(self.__btn_prev_song)

        self.__btn_play_song = IconButton.build(
            padding=Paddings.RELATIVE_50,
            size=Icons.X_LARGE,
            style=IconButtonStyle(
                light_mode_icon=Icons.PLAY.with_color(Colors.PRIMARY),
                dark_mode_icon=Icons.PLAY.with_color(Colors.WHITE),
                light_mode_background=Backgrounds.CIRCLE_PRIMARY_10,
                dark_mode_background=Backgrounds.CIRCLE_PRIMARY,
            ),
        )
        self.__play_buttons.addWidget(self.__btn_play_song)

        self.__btn_pause_song = IconButton.build(
            padding=Paddings.RELATIVE_50,
            size=Icons.X_LARGE,
            style=IconButtonStyle(
                light_mode_icon=Icons.PAUSE.with_color(Colors.PRIMARY),
                dark_mode_icon=Icons.PAUSE.with_color(Colors.WHITE),
                light_mode_background=Backgrounds.CIRCLE_PRIMARY_10,
                dark_mode_background=Backgrounds.CIRCLE_PRIMARY,
            )
        )
        self.__play_buttons.addWidget(self.__btn_pause_song)

        self.__btn_next_song = IconButton.build(
            padding=Paddings.RELATIVE_50,
            size=Icons.LARGE,
            style=IconButtonStyle(
                light_mode_icon=Icons.NEXT.with_color(Colors.PRIMARY),
                light_mode_background=Backgrounds.CIRCLE_HIDDEN_PRIMARY_10,
            )
        )
        self.__play_buttons.addWidget(self.__btn_next_song)

    @override
    def assign_shortcuts(self) -> None:
        play_shortcut = QShortcut(QKeySequence(Qt.Key_Space), self.__btn_play_song)
        play_shortcut.activated.connect(self.__btn_play_song.click)

        pause_shortcut = QShortcut(QKeySequence(Qt.Key_Space), self.__btn_pause_song)
        pause_shortcut.activated.connect(self.__btn_pause_song.click)

        prev_shortcut = QShortcut(QKeySequence(Qt.Key_Left), self.__btn_prev_song)
        prev_shortcut.activated.connect(self.__btn_prev_song.click)

        next_shortcut = QShortcut(QKeySequence(Qt.Key_Right), self.__btn_next_song)
        next_shortcut.activated.connect(self.__btn_next_song.click)

    @override
    def apply_light_mode(self) -> None:
        self.__btn_next_song.apply_light_mode()
        self.__btn_prev_song.apply_light_mode()
        self.__btn_play_song.apply_light_mode()
        self.__btn_pause_song.apply_light_mode()
        self.__label_song_title.apply_light_mode()
        self.__label_song_artist.apply_light_mode()

    @override
    def apply_dark_mode(self) -> None:
        self.__btn_next_song.apply_dark_mode()
        self.__btn_prev_song.apply_dark_mode()
        self.__btn_play_song.apply_dark_mode()
        self.__btn_pause_song.apply_dark_mode()
        self.__label_song_title.apply_dark_mode()
        self.__label_song_artist.apply_dark_mode()

    @connector
    def set_onclick_prev_song(self, fn: callable) -> None:
        self.__btn_prev_song.clicked.connect(lambda: fn())

    @connector
    def set_onclick_play_song(self, fn: callable) -> None:
        self.__btn_play_song.clicked.connect(lambda: self.__onclick_play(fn))

    @connector
    def set_onclick_pause_song(self, fn: callable) -> None:
        self.__btn_pause_song.clicked.connect(lambda: self.__onclick_pause(fn))

    def __onclick_play(self, fn: callable) -> None:
        self.set_is_playing(True)
        fn()

    def __onclick_pause(self, fn: callable) -> None:
        self.set_is_playing(False)
        fn()

    @connector
    def set_onclick_next_song(self, fn: callable) -> None:
        self.__btn_next_song.clicked.connect(lambda: fn())

    def set_default_cover(self, byte_pixmap: bytes) -> None:
        cover = self.__create_cover(byte_pixmap)
        self.__song_cover.set_default_cover(cover)

    def set_default_title(self, text: str) -> None:
        self.__label_song_title.set_default_text(text)

    def set_default_artist(self, text: str) -> None:
        self.__label_song_artist.set_default_text(text)

    def set_cover(self, byte_pixmap: bytes) -> None:
        self.__song_cover.set_cover(self.__create_cover(byte_pixmap))

    def set_title(self, text: str) -> None:
        self.__label_song_title.setText(text)

    def set_artist(self, text: str) -> None:
        self.__label_song_artist.setText(text)

    def set_is_playing(self, enable: bool) -> None:
        self.__btn_play_song.setVisible(not enable)
        self.__btn_pause_song.setVisible(enable)

    def is_playing(self) -> bool:
        return self.__btn_pause_song.isVisible()

    @staticmethod
    def __create_cover(byte_pixmap: bytes) -> Union[CoverProp, None]:
        if byte_pixmap is None:
            return None
        return CoverProp.from_bytes(byte_pixmap, width=64, height=64, radius=16)
