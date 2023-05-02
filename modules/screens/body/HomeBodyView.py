from typing import Optional, Callable

from PyQt5.QtGui import QShowEvent
from PyQt5.QtWidgets import QScrollArea, QWidget, QVBoxLayout

from modules.helpers.types.Decorators import override, connector
from modules.models.Playlist import Playlist
from modules.screens.AbstractScreen import BaseView
from modules.screens.body.CurrentPlaylistView import CurrentPlaylistView
from modules.screens.body.PlaylistCarouselView import PlaylistCarouselView, PlaylistCardData
from modules.statics.view.Material import Backgrounds


class HomeBodyView(QScrollArea, BaseView):
    __inner: QWidget
    __main_layout: QVBoxLayout
    __playlist_carousel: PlaylistCarouselView
    __current_playlist: CurrentPlaylistView

    def __init__(self, parent: Optional["QWidget"] = None):
        super(HomeBodyView, self).__init__(parent)
        self.__init_ui()

    def __init_ui(self) -> None:
        self.setStyleSheet(Backgrounds.TRANSPARENT.to_stylesheet())
        self.__inner = QWidget()
        self.setWidget(self.__inner)

        self.__main_layout = QVBoxLayout(self.__inner)
        self.__main_layout.setContentsMargins(0, 0, 0, 0)
        self.__main_layout.setSpacing(50)

        self.__playlist_carousel = PlaylistCarouselView()
        self.__playlist_carousel.setFixedHeight(360)
        self.__playlist_carousel.setStyleSheet(Backgrounds.TRANSPARENT.to_stylesheet())

        self.__current_playlist = CurrentPlaylistView()

        self.__main_layout.addWidget(self.__playlist_carousel)
        self.__main_layout.addWidget(self.__current_playlist)

    @override
    def setContentsMargins(self, left: int, top: int, right: int, bottom: int) -> None:
        self.__playlist_carousel.setContentsMargins(left, top, right, bottom)
        self.__current_playlist.setContentsMargins(left, top, right, bottom)

    @override
    def showEvent(self, event: QShowEvent) -> None:
        self.__current_playlist.setFixedHeight(self.height())
        return super().showEvent(event)

    @override
    def apply_light_mode(self) -> None:
        self.__playlist_carousel.apply_light_mode()
        self.__current_playlist.apply_light_mode()

    @override
    def apply_dark_mode(self) -> None:
        self.__playlist_carousel.apply_dark_mode()
        self.__current_playlist.apply_dark_mode()

    @connector
    def set_onclick_play(self, fn: Callable[[int], None]) -> None:
        self.__current_playlist.set_onclick_play(fn)

    @connector
    def set_onclick_love(self, fn: Callable[[int], None]) -> None:
        self.__current_playlist.set_onclick_love(fn)

    @connector
    def set_onclick_add_to_playlist(self, fn: Callable[[int], None]) -> None:
        self.__current_playlist.set_onclick_add_to_playlist_on_menu(fn)

    @connector
    def set_onclick_remove_from_playlist(self, fn: Callable[[int], None]) -> None:
        self.__current_playlist.set_onclick_remove_from_playlist_on_menu(fn)

    @connector
    def set_onchange_song_title_and_artist_on_menu(self, fn: Callable[[int, str, str], bool]) -> None:
        self.__current_playlist.set_onchange_song_title_and_artist_on_menu(fn)

    @connector
    def set_on_change_song_cover_on_menu(self, fn: Callable[[int, str], None]) -> None:
        self.__current_playlist.set_onchange_song_cover_on_menu(fn)

    @connector
    def set_on_delete_song_on_menu(self, fn: Callable[[int], None]) -> None:
        self.__current_playlist.set_on_delete_song_on_menu(fn)

    @connector
    def set_on_keypress(self, fn: Callable[[str], int]) -> None:
        self.__current_playlist.set_on_keypress(fn)

    @connector
    def set_onclose_download_dialog(self, fn: callable) -> None:
        self.__current_playlist.set_onclose_download_dialog(fn)

    @connector
    def set_onclick_download_songs_to_library_fn(self, fn: Callable[[str], None]) -> None:
        self.__current_playlist.set_onclick_download_songs_to_library_fn(fn)

    @connector
    def set_onclick_add_songs_to_library_fn(self, fn: Callable[[list[str]], None]) -> None:
        self.__current_playlist.set_onclick_add_songs_to_library_fn(fn)

    @connector
    def set_onclick_select_songs_to_playlist_fn(self, fn: Callable[[], None]) -> None:
        self.__current_playlist.set_onclick_select_songs_to_playlist_fn(fn)

    @connector
    def set_onclick_apply_select_songs_to_playlist_fn(self, fn: Callable[[], None]) -> None:
        self.__current_playlist.set_onclick_apply_select_songs_to_playlist_fn(fn)

    def add_download_item(self, label: str) -> None:
        self.__current_playlist.add_download_item(label)

    def set_description_in_download_dialog_at(self, index: int, value: str) -> None:
        self.__current_playlist.set_description_in_download_dialog_at(index, value)

    def set_progress_in_download_dialog_at(self, index: int, value: float) -> None:
        self.__current_playlist.set_progress_in_download_dialog_at(index, value)

    @connector
    def set_onclick_library(self, fn: Callable[[], None]) -> None:
        self.__playlist_carousel.set_onclick_library(fn)

    @connector
    def set_onclick_favourites(self, fn: Callable[[], None]) -> None:
        self.__playlist_carousel.set_onclick_favourites(fn)

    @connector
    def set_onclick_add_playlist(self, fn: Callable[[], None]) -> None:
        self.__playlist_carousel.set_onclick_add_playlist(fn)

    def enable_choosing_song(self, is_choosing: bool) -> None:
        self.__current_playlist.enable_choosing_song(is_choosing)

    def enable_add_songs_to_library(self, visible: bool) -> None:
        self.__current_playlist.enable_add_songs_to_library(visible)

    def enable_select_songs_to_playlist(self, visible: bool) -> None:
        self.__current_playlist.enable_select_songs_to_playlist(visible)

    def set_default_playlist_cover(self, cover: bytes) -> None:
        self.__playlist_carousel.set_default_playlist_cover(cover)

    def load_playlists(self, playlists: list[PlaylistCardData]) -> None:
        self.__playlist_carousel.load_playlists(playlists)

    def add_playlist(self, playlist: PlaylistCardData) -> None:
        self.__playlist_carousel.add_playlist(playlist)

    def delete_playlist(self, playlist: PlaylistCardData) -> None:
        self.__playlist_carousel.delete_playlist(playlist)

    def update_playlist(self, playlist: PlaylistCardData) -> None:
        self.__playlist_carousel.update_playlist(playlist)

    def select_song_at(self, index: int) -> None:
        self.__current_playlist.select_song_at(index)

    def enable_edit_songs(self, enabled: bool) -> None:
        self.__current_playlist.enable_edit_songs(enabled)

    def enable_delete_songs(self, enabled: bool) -> None:
        self.__current_playlist.enable_delete_songs(enabled)

    def enable_edit_of_song_at(self, index: int, enabled: bool) -> None:
        self.__current_playlist.enable_edit_of_song_at(index, enabled)

    def enable_delete_song_at(self, index: int, enabled: bool) -> None:
        self.__current_playlist.enable_delete_song_at(index, enabled)

    def refresh_menu(self) -> None:
        self.__current_playlist.refresh_menu()

    def love_song(self, is_loved: bool) -> None:
        self.__current_playlist.love_song(is_loved)

    def load_playlist(self, playlist: Playlist) -> None:
        self.__current_playlist.load_playlist(playlist)

    def set_playlist_info(self, playlist: Playlist) -> None:
        self.__current_playlist.set_current_playlist_info(playlist)

    def load_choosing_playlist(self, playlist: Playlist) -> None:
        self.__current_playlist.load_choosing_playlist(playlist)
