from modules.helpers import LibraryHelper
from modules.helpers.types.Bytes import Bytes
from modules.helpers.types.Decorators import override
from modules.models.AudioPlayer import AudioPlayer
from modules.models.Playlist import Playlist
from modules.models.PlaylistInformation import PlaylistInformation
from modules.models.PlaylistSongs import PlaylistSongs
from modules.models.Song import Song
from modules.screens.AbstractScreen import BaseControl
from modules.screens.body.PlaylistCarouselView import PlaylistCardData
from modules.screens.windows.MainWindowView import MainWindowView
from modules.statics.view.Material import Images


class MainWindowControl(MainWindowView, BaseControl):
    __library: Playlist
    __displaying_playlist: Playlist = None
    __playing_playlist: Playlist = None
    __playlists: list[Playlist]
    __player: AudioPlayer = AudioPlayer()
    __selecting_playlist_songs: set[int]

    def __init__(self) -> None:
        super().__init__()
        self.__playlists = []
        self.__selecting_playlist_songs = set()
        self.set_default_playlist_cover(Images.DEFAULT_PLAYLIST_COVER)
        self.connect_signals()
        self.set_is_playing(False)

    @override
    def connect_signals(self) -> None:
        self._music_player.set_onclick_play(lambda index: self.__play_song_from_player_at(index))
        self._music_player.set_onclick_pause(lambda index: self.set_is_playing(False))
        self._music_player.set_onclick_shuffle(lambda: self._body.refresh_menu())
        self._music_player.set_onclick_love(lambda song: self.__love_song_from_player(song))

        self._body.set_onclick_play(lambda index: self.__play_song_from_menu_at(index))
        self._body.set_onclick_love(lambda index: self.__love_song_from_menu(index))
        self._body.set_onclick_add_to_playlist(lambda index: self.__add_song_from_menu_at(index))
        self._body.set_onclick_remove_from_playlist(lambda index: self.__remove_song_from_menu_at(index))
        self._body.set_onclick_select_songs_fn(lambda: self.__start_select_songs_from_library_to_playlist())
        self._body.set_onclick_apply_select_songs_fn(lambda: self.__finish_select_songs_from_library_to_playlist())
        self._body.set_on_keypress(lambda key: self.__go_to_song_that_title_start_with(key))

        self._body.set_onclick_library(self.__choose_library)
        self._body.set_onclick_favourites(self.__choose_favourites)
        self._body.set_onclick_add_playlist(self.__create_empty_playlist)

        self.set_onclick_close(lambda: self._music_player.pause_current_song())
        self.set_onclick_play_on_tray(lambda: self._music_player.play_current_song())
        self.set_onclick_pause_on_tray(lambda: self._music_player.pause_current_song())
        self.set_onclick_prev_on_tray(lambda: self._music_player.play_previous_song())
        self.set_onclick_next_on_tray(lambda: self._music_player.play_next_song())

    def load_library(self, playlist: Playlist) -> None:
        self.__library = playlist
        self.__show_library_on_menu_and_player()

    def load_playlists(self, playlists: list[Playlist]) -> None:
        self.__playlists.clear()
        for playlist in playlists:
            self.__create_playlist(playlist)

    def __choose_library(self) -> None:
        self._body.enable_choosing_song(False)
        self._body.enable_add_new_song(False)
        self.__select_playlist(self.__library)

    def __choose_favourites(self) -> None:
        self._body.enable_choosing_song(False)
        self._body.enable_add_new_song(False)

        favourite_songs: list[Song] = list(filter(lambda song: song.is_loved(), self.__library.get_songs().get_songs()))
        playlist = Playlist.create(name="Favourites", songs=PlaylistSongs(favourite_songs))
        self.__select_playlist(playlist)

    def __choose_playlist(self, playlist: Playlist) -> None:
        self._body.enable_choosing_song(False)
        self._body.enable_add_new_song(True)
        self.__select_playlist(playlist)

    def __select_playlist(self, playlist: Playlist) -> None:
        self.__selecting_playlist_songs.clear()
        self.__displaying_playlist = playlist
        self._body.load_playlist(playlist)

    def __create_empty_playlist(self) -> None:
        empty_playlist = Playlist(
            info=PlaylistInformation(name="Untitled", cover=Images.DEFAULT_PLAYLIST_COVER),
            songs=PlaylistSongs()
        )
        self.__create_playlist(empty_playlist)

    def __create_playlist(self, playlist: Playlist) -> None:
        card = PlaylistCardData(playlist.get_info())
        card.set_onclick(lambda: self.__choose_playlist(playlist))
        card.set_onchange_title(lambda title: self.__update_playlist_name(card, title))
        card.set_onchange_cover(lambda cover_path: self.__update_playlist_cover(card, cover_path))
        card.set_ondelete(lambda: self.__delete_playlist(card))
        self._body.add_playlist(card)

        playlist: Playlist = Playlist(info=playlist.get_info(), songs=playlist.get_songs())
        self.__playlists.append(playlist)

    def __update_playlist_name(self, card: PlaylistCardData, name: str) -> None:
        card.content().name = name
        self.__update_display_playlist_info_if_updating(card)
        LibraryHelper.save_playlists(self.__playlists)

    def __update_playlist_cover(self, card: PlaylistCardData, cover_path: str) -> None:
        card.content().cover = Bytes.get_bytes_from_file(cover_path)
        self._body.update_playlist(card)
        self.__update_display_playlist_info_if_updating(card)
        LibraryHelper.save_playlists(self.__playlists)

    def __update_display_playlist_info_if_updating(self, card):
        updating_playlist: Playlist = self.find_playlist_of(card)
        if updating_playlist == self.__displaying_playlist:
            self._body.set_playlist_info(self.__displaying_playlist)

    def __delete_playlist(self, card: PlaylistCardData) -> None:
        self._body.delete_playlist(card)
        item_to_delete: Playlist = self.find_playlist_of(card)
        self.__playlists.remove(item_to_delete)

        """
            We will switch back to library if delete playing playlist
        """
        if item_to_delete == self.__playing_playlist:
            self.__show_library_on_menu_and_player()
            self._music_player.stop_current_song()

        LibraryHelper.save_playlists(self.__playlists)

    def __show_library_on_menu_and_player(self):
        self.__choose_library()
        self._music_player.load_playlist_songs(self.__displaying_playlist.get_songs())
        self._music_player.load_playing_song()

    def find_playlist_of(self, card: PlaylistCardData) -> Playlist:
        return next(playlist_ for playlist_ in self.__playlists if playlist_.get_info().id == card.content().id)

    def __start_select_songs_from_library_to_playlist(self) -> None:
        current_playlist_songs_ids: list[str] = [song.get_id() for song in
                                                 self.__displaying_playlist.get_songs().get_songs()]
        temp_songs = [song.clone() for song in self.__library.get_songs().get_songs()]
        """
            We will consider loved songs as the existing songs
        """
        for index, song in enumerate(temp_songs):
            is_existing = song.get_id() in current_playlist_songs_ids
            song.set_love_state(is_existing)
            if is_existing:
                self.__selecting_playlist_songs.add(index)

        self._body.enable_choosing_song(True)
        temp_playlist: Playlist = Playlist(info=self.__displaying_playlist.get_info(), songs=PlaylistSongs(temp_songs))

        self._body.load_choosing_playlist(temp_playlist)

    def __finish_select_songs_from_library_to_playlist(self) -> None:
        playlist_songs = [song for index, song in enumerate(self.__library.get_songs().get_songs()) if
                          index in self.__selecting_playlist_songs]
        self.__selecting_playlist_songs.clear()

        self.__displaying_playlist.get_songs().get_songs().clear()
        self.__displaying_playlist.get_songs().insertAll(playlist_songs)
        LibraryHelper.save_playlists(self.__playlists)
        self.__choose_playlist(self.__displaying_playlist)

    def __add_song_from_menu_at(self, index: int) -> None:
        self.__selecting_playlist_songs.add(index)

    def __remove_song_from_menu_at(self, index: int) -> None:
        self.__selecting_playlist_songs.remove(index)

    def __love_song_from_player(self, song: Song) -> None:
        self._body.love_song(song.is_loved())
        LibraryHelper.update_love_state_of(song)

    def __love_song_from_menu(self, index: int) -> None:
        if self.__player.get_current_song_index() == index:
            self._music_player.change_love_state()
            return
        song = self.__displaying_playlist.get_songs().get_song_at(index)
        song.reverse_love_state()
        LibraryHelper.update_love_state_of(self.__player.get_songs()[index])

    def __play_song_from_player_at(self, index: int) -> None:
        self._body.select_song_at(index)
        self.set_is_playing(True)

    def __play_song_from_menu_at(self, index: int) -> None:
        self._music_player.load_playlist_songs(self.__displaying_playlist.get_songs())
        self.__playing_playlist = self.__displaying_playlist
        self._music_player.play_song_at(index)
        self.set_is_playing(True)

    def __go_to_song_that_title_start_with(self, title: str) -> int:
        return self.__displaying_playlist.get_songs().find_nearest_song_index_by_title(title)
