from typing import Optional, Callable

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QFileDialog, QVBoxLayout

from modules.helpers.types.Decorators import override, connector
from modules.models.view.Background import Background
from modules.models.view.Border import Border
from modules.models.view.Color import Color
from modules.models.view.ColorBox import ColorBox
from modules.models.view.Padding import Padding
from modules.models.view.builder.FontBuilder import FontBuilder
from modules.models.view.builder.IconButtonStyle import IconButtonStyle
from modules.models.view.builder.TextStyle import TextStyle
from modules.screens.AbstractScreen import BaseView
from modules.statics.view.Material import ColorBoxes, Icons, Paddings, Colors, Backgrounds, Images
from modules.widgets import Dialogs
from modules.widgets.Buttons import IconButton, ActionButton
from modules.widgets.Cover import CoverProp, Cover
from modules.widgets.Dialogs import Dialog
from modules.widgets.Icons import AppIcon
from modules.widgets.Labels import LabelWithDefaultText, Input


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

        self.__view_layout = QVBoxLayout(self)
        self.__view_layout.setAlignment(Qt.AlignVCenter)
        self.__view_layout.addWidget(self.__image)
        self.__view_layout.addWidget(self.__header)
        self.__view_layout.addSpacing(4)
        self.__view_layout.addWidget(self.__input)
        self.__view_layout.addSpacing(8)
        self.__view_layout.addWidget(self.__accept_btn)

        self.__image.set_cover(CoverProp.from_bytes(Images.DOWNLOAD, width=128))
        self.__header.setText("Download Youtube Song")
        self.__accept_btn.setText("Download")

        self.setFixedWidth(480)
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


class SongTableHeaderView(QWidget, BaseView):
    __main_layout: QHBoxLayout
    __info: QHBoxLayout

    __label_track: LabelWithDefaultText
    __label_artist: LabelWithDefaultText
    __label_length: LabelWithDefaultText

    __buttons: QWidget
    __buttons_layout: QHBoxLayout
    __btn_download_songs: IconButton
    __btn_select_songs: IconButton

    __onclick_add_songs_to_library_fn: Callable[[list[str]], None]
    __on_download_songs_to_library_fn: Callable[[str], None]
    __onclick_select_songs_to_playlist_fn: Callable[[], None]
    __onclick_apply_select_songs_to_playlist_fn: Callable[[], None]

    def __init__(self, parent: Optional["QWidget"] = None):
        super(SongTableHeaderView, self).__init__(parent)
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
        self.__buttons.setMinimumWidth(185)
        self.__buttons_layout = QHBoxLayout(self.__buttons)
        self.__buttons_layout.setAlignment(Qt.AlignRight)
        self.__buttons_layout.setSpacing(8)
        self.__buttons_layout.setContentsMargins(8, 0, 8, 0)

        self.__buttons_layout.addSpacing(48)
        self.__buttons_layout.addSpacing(8)

        self.__btn_download_songs = self.__create_button(Icons.DOWNLOAD, Paddings.RELATIVE_50)
        self.__btn_download_songs.clicked.connect(self.show_download_dialog)
        self.__buttons_layout.addWidget(self.__btn_download_songs)

        self.__btn_add_songs_to_library = self.__create_button(Icons.ADD, Paddings.RELATIVE_67)
        self.__btn_add_songs_to_library.clicked.connect(lambda: self.__select_song_paths_to_add_to_library())
        self.__buttons_layout.addWidget(self.__btn_add_songs_to_library)

        self.__btn_select_songs = self.__create_button(Icons.EDIT, Paddings.RELATIVE_67)
        self.__btn_select_songs.clicked.connect(lambda: self.__onclick_select_songs_to_playlist_fn())
        self.__buttons_layout.addWidget(self.__btn_select_songs)

        self.__btn_apply_add_songs = self.__create_button(Icons.APPLY, Paddings.RELATIVE_50)
        self.__btn_apply_add_songs.clicked.connect(lambda: self.__onclick_apply_select_songs_to_playlist_fn())
        self.__btn_apply_add_songs.hide()
        self.__buttons_layout.addWidget(self.__btn_apply_add_songs)

        self.__info.addWidget(self.__label_track)
        self.__info.addStretch(1)
        self.__info.addSpacing(24)
        self.__info.addWidget(self.__label_artist, 1)
        self.__info.addWidget(self.__label_length)
        self.__info.addWidget(self.__buttons)

    def show_download_dialog(self) -> None:
        dialog = DownloadDialog()
        dialog.on_download(lambda url: self.__on_download_songs_to_library_fn(url))
        Dialogs.Dialogs.show_dialog(dialog)

    def __select_song_paths_to_add_to_library(self) -> None:
        paths = QFileDialog.getOpenFileNames(self, filter="MP3 (*.MP3 *.mp3)")[0]
        if paths is not None and len(paths) > 0:
            return self.__onclick_add_songs_to_library_fn(paths)

    @override
    def apply_light_mode(self) -> None:
        self.__label_track.apply_light_mode()
        self.__label_artist.apply_light_mode()
        self.__label_length.apply_light_mode()
        self.__btn_download_songs.apply_light_mode()
        self.__btn_add_songs_to_library.apply_light_mode()
        self.__btn_select_songs.apply_light_mode()
        self.__btn_apply_add_songs.apply_light_mode()

    @override
    def apply_dark_mode(self) -> None:
        self.__label_track.apply_dark_mode()
        self.__label_artist.apply_dark_mode()
        self.__label_length.apply_dark_mode()
        self.__btn_download_songs.apply_dark_mode()
        self.__btn_add_songs_to_library.apply_dark_mode()
        self.__btn_select_songs.apply_dark_mode()
        self.__btn_apply_add_songs.apply_dark_mode()

    @override
    def setText(self, track: str = "TRACK", artist: str = "ARTIST", length: str = "LENGTH") -> None:
        self.__label_track.setText(track)
        self.__label_artist.setText(artist)
        self.__label_length.setText(length)

    def enable_choosing_song(self, is_choosing: bool) -> None:
        self.__btn_apply_add_songs.setVisible(is_choosing)
        self.__btn_select_songs.setVisible(not is_choosing)

    def enable_add_songs_to_library(self, visible: bool) -> None:
        if visible:
            self.__btn_add_songs_to_library.setVisible(True)
        else:
            self.__btn_add_songs_to_library.setVisible(False)

    def enable_select_songs_to_playlist(self, visible: bool) -> None:
        if visible:
            self.__btn_select_songs.setVisible(True)
            self.__btn_apply_add_songs.setVisible(False)
        else:
            self.__btn_select_songs.setVisible(False)
            self.__btn_apply_add_songs.setVisible(False)

    def set_onclick_download_songs_to_library_fn(self, fn: Callable[[str], None]) -> None:
        self.__on_download_songs_to_library_fn = fn

    def set_onclick_add_songs_to_library_fn(self, fn: Callable[[list[str]], None]) -> None:
        self.__onclick_add_songs_to_library_fn = fn

    def set_onclick_select_songs_to_playlist_fn(self, fn: Callable[[], None]) -> None:
        self.__onclick_select_songs_to_playlist_fn = fn

    def set_onclick_apply_select_songs_to_playlist_fn(self, fn: Callable[[], None]) -> None:
        self.__onclick_apply_select_songs_to_playlist_fn = fn

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
