from typing import Optional, Callable

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QFileDialog

from modules.helpers.types.Decorators import override
from modules.models.view.Padding import Padding
from modules.models.view.builder.FontBuilder import FontBuilder
from modules.models.view.builder.IconButtonStyle import IconButtonStyle
from modules.models.view.builder.TextStyle import TextStyle
from modules.screens.AbstractScreen import BaseView
from modules.screens.body.songs_table.DownloadDialog import DownloadDialog
from modules.statics.view.Material import ColorBoxes, Icons, Paddings, Colors, Backgrounds
from modules.widgets.Buttons import IconButton
from modules.widgets.Icons import AppIcon
from modules.widgets.Labels import LabelWithDefaultText


class SongTableHeaderView(QWidget, BaseView):
    __main_layout: QHBoxLayout
    __info: QHBoxLayout

    __label_track: LabelWithDefaultText
    __label_artist: LabelWithDefaultText
    __label_length: LabelWithDefaultText

    __buttons: QWidget
    __buttons_layout: QHBoxLayout
    __btn_download_songs_to_library: IconButton
    __btn_select_songs: IconButton

    __onclick_add_songs_to_library_fn: Callable[[list[str]], None]
    __on_download_songs_to_library_fn: Callable[[str], None]
    __onclick_select_songs_to_playlist_fn: Callable[[], None]
    __onclick_apply_select_songs_to_playlist_fn: Callable[[], None]

    def __init__(self, parent: Optional["QWidget"] = None):
        super(SongTableHeaderView, self).__init__(parent)
        self.__init_ui()

    def __init_ui(self) -> None:
        self.__download_dialog = DownloadDialog()
        self.__download_dialog.on_download(lambda url: self.__on_download_songs_to_library_fn(url))

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

        self.__btn_download_songs_to_library = self.__create_button(Icons.DOWNLOAD, Paddings.RELATIVE_50)
        self.__btn_download_songs_to_library.clicked.connect(self.__download_dialog.show)
        self.__btn_download_songs_to_library.setToolTip("Download songs from Youtube.")
        self.__buttons_layout.addWidget(self.__btn_download_songs_to_library)

        self.__btn_add_songs_to_library = self.__create_button(Icons.ADD, Paddings.RELATIVE_67)
        self.__btn_add_songs_to_library.clicked.connect(lambda: self.__select_song_paths_to_add_to_library())
        self.__btn_add_songs_to_library.setToolTip("Import songs from computer.")
        self.__buttons_layout.addWidget(self.__btn_add_songs_to_library)

        self.__btn_select_songs = self.__create_button(Icons.EDIT, Paddings.RELATIVE_67)
        self.__btn_select_songs.clicked.connect(lambda: self.__clicked_select_songs())
        self.__btn_select_songs.setToolTip("Select playlist songs.")
        self.__buttons_layout.addWidget(self.__btn_select_songs)

        self.__btn_apply_add_songs = self.__create_button(Icons.APPLY, Paddings.RELATIVE_50)
        self.__btn_apply_add_songs.clicked.connect(lambda: self.clicked_apply_songs())
        self.__btn_apply_add_songs.hide()
        self.__buttons_layout.addWidget(self.__btn_apply_add_songs)

        self.__info.addWidget(self.__label_track)
        self.__info.addStretch(1)
        self.__info.addSpacing(24)
        self.__info.addWidget(self.__label_artist, 1)
        self.__info.addWidget(self.__label_length)
        self.__info.addWidget(self.__buttons)

    def clicked_apply_songs(self) -> None:
        self.__btn_select_songs.show()
        self.__btn_apply_add_songs.hide()
        return self.__onclick_apply_select_songs_to_playlist_fn()

    def __clicked_select_songs(self) -> None:
        self.__btn_select_songs.hide()
        self.__btn_apply_add_songs.show()
        return self.__onclick_select_songs_to_playlist_fn()

    def __select_song_paths_to_add_to_library(self) -> None:
        paths = QFileDialog.getOpenFileNames(self, filter="MP3 (*.MP3 *.mp3)")[0]
        if paths is not None and len(paths) > 0:
            return self.__onclick_add_songs_to_library_fn(paths)

    @override
    def apply_light_mode(self) -> None:
        self.__label_track.apply_light_mode()
        self.__label_artist.apply_light_mode()
        self.__label_length.apply_light_mode()
        self.__btn_download_songs_to_library.apply_light_mode()
        self.__btn_add_songs_to_library.apply_light_mode()
        self.__btn_select_songs.apply_light_mode()
        self.__btn_apply_add_songs.apply_light_mode()

    @override
    def apply_dark_mode(self) -> None:
        self.__label_track.apply_dark_mode()
        self.__label_artist.apply_dark_mode()
        self.__label_length.apply_dark_mode()
        self.__btn_download_songs_to_library.apply_dark_mode()
        self.__btn_add_songs_to_library.apply_dark_mode()
        self.__btn_select_songs.apply_dark_mode()
        self.__btn_apply_add_songs.apply_dark_mode()

    @override
    def setText(self, track: str = "TRACK", artist: str = "ARTIST", length: str = "LENGTH") -> None:
        self.__label_track.setText(track)
        self.__label_artist.setText(artist)
        self.__label_length.setText(length)

    def enable_choosing_song(self, is_choosing: bool) -> None:
        if is_choosing:
            self.__btn_select_songs.setVisible(True)
            self.__btn_apply_add_songs.setVisible(False)
        else:
            self.__btn_apply_add_songs.setVisible(False)
            self.__btn_select_songs.setVisible(False)

    def enable_add_songs_to_library(self, visible: bool) -> None:
        if visible:
            self.__btn_add_songs_to_library.setVisible(True)
        else:
            self.__btn_add_songs_to_library.setVisible(False)

    def enable_download_songs_to_library(self, visible: bool) -> None:
        if visible:
            self.__btn_download_songs_to_library.setVisible(True)
        else:
            self.__btn_download_songs_to_library.setVisible(False)

    def enable_select_songs_to_playlist(self, visible: bool) -> None:
        if visible:
            self.__btn_select_songs.setVisible(True)
            self.__btn_apply_add_songs.setVisible(False)
        else:
            self.__btn_select_songs.setVisible(False)
            self.__btn_apply_add_songs.setVisible(False)

    def set_onclose_download_dialog(self, fn: callable) -> None:
        self.__download_dialog.on_close(fn)

    def set_onclick_download_songs_to_library_fn(self, fn: Callable[[str], None]) -> None:
        self.__on_download_songs_to_library_fn = fn

    def set_onclick_add_songs_to_library_fn(self, fn: Callable[[list[str]], None]) -> None:
        self.__onclick_add_songs_to_library_fn = fn

    def set_onclick_select_songs_to_playlist_fn(self, fn: Callable[[], None]) -> None:
        self.__onclick_select_songs_to_playlist_fn = fn

    def set_onclick_apply_select_songs_to_playlist_fn(self, fn: Callable[[], None]) -> None:
        self.__onclick_apply_select_songs_to_playlist_fn = fn

    def add_item(self, label: str) -> None:
        self.__download_dialog.add_item(label)

    def mark_succeed_at(self, index: int) -> None:
        self.__download_dialog.mark_succeed_at(index)

    def mark_processing_at(self, index: int) -> None:
        self.__download_dialog.mark_processing_at(index)

    def mark_failed_at(self, index: int) -> None:
        self.__download_dialog.mark_failed_at(index)

    def set_description_at(self, index: int, value: str) -> None:
        self.__download_dialog.set_description_at(index, value)

    def set_progress_at(self, index: int, value: float) -> None:
        self.__download_dialog.set_progress_at(index, value)

    def is_opening_download_dialog(self) -> bool:
        return self.__download_dialog.isVisible()

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
