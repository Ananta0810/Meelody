from modules.helpers import LibraryHelper
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
    __playlist: Playlist
    __playlists: list[Playlist]
    __player: AudioPlayer = AudioPlayer()

    def __init__(self) -> None:
        super().__init__()
        self.__playlists = []
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
        self._body.set_onclick_love(lambda index: self.love_song_from_menu(index))
        self._body.set_on_keypress(lambda key: self.__go_to_song_that_title_start_with(key))
        self._body.set_onclick_add_song_fn(lambda: self.__start_add_songs_from_library_to_playlist())
        self._body.set_onclick_apply_add_song_fn(lambda: self.__finish_add_songs_from_library_to_playlist())

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
        self.__choose_library()
        self._music_player.load_playing_song()

    def load_playlists(self, playlists: list[Playlist]) -> None:
        self.__playlists.clear()
        for playlist in playlists:
            self.__create_playlist(playlist)

    def __choose_library(self) -> None:
        self.__load_playlist(self.__library)

    def __choose_favourites(self) -> None:
        favourite_songs: list[Song] = list(filter(lambda song: song.is_loved(), self.__library.get_songs().get_songs()))
        playlist = Playlist.create(name="Favourites", songs=PlaylistSongs(favourite_songs))
        self.__load_playlist(playlist)

    def __choose_playlist(self, playlist: Playlist) -> None:
        self.__load_playlist(playlist)

    def __load_playlist(self, playlist: Playlist) -> None:
        self.__playlist = playlist
        self._music_player.load_playlist_songs(playlist.get_songs())
        self._body.load_playlist(playlist)

    def __create_empty_playlist(self) -> None:
        empty_playlist = Playlist(
            info=PlaylistInformation(name="Untitled", cover=Images.DEFAULT_PLAYLIST_COVER),
            songs=PlaylistSongs()
        )
        self.__create_playlist(empty_playlist)

    def __create_playlist(self, playlist: Playlist) -> None:
        card = PlaylistCardData(playlist.get_info())
        card.set_ondelete(lambda: self.__delete_playlist(card))
        card.set_onchange_title(lambda title: self.__update_playlist_name(card, title))
        card.set_onclick(lambda: self.__choose_playlist(playlist))
        self._body.add_playlist(card)

        playlist: Playlist = Playlist(info=playlist.get_info(), songs=playlist.get_songs())
        self.__playlists.append(playlist)

    def __update_playlist_name(self, playlist: PlaylistCardData, title: str) -> None:
        playlist.content().name = title
        LibraryHelper.save_playlists(self.__playlists)

    def __delete_playlist(self, playlist: PlaylistCardData) -> None:
        self._body.delete_playlist(playlist)
        item_to_delete = next(playlist_ for playlist_ in self.__playlists if playlist_.get_info().id == playlist.content().id)
        self.__playlists.remove(item_to_delete)
        LibraryHelper.save_playlists(self.__playlists)

    def __start_add_songs_from_library_to_playlist(self) -> None:
        self.__choose_library()
        self._body.set_choosing_song(True)

    def __finish_add_songs_from_library_to_playlist(self) -> None:
        self._body.set_choosing_song(False)

    def love_song_at(self, index: int) -> None:
        if self.__player.get_current_song_index() == index:
            self._music_player.change_love_state()
            return
        song = self.__playlist.get_songs().get_song_at(index)
        song.reverse_love_state()

    def __love_song_from_player(self, song: Song) -> None:
        self._body.love_song(song.is_loved())
        LibraryHelper.update_love_state_of(song)

    def love_song_from_menu(self, index: int) -> None:
        self.love_song_at(index)
        LibraryHelper.update_love_state_of(self.__player.get_songs()[index])

    def __play_song_from_player_at(self, index: int) -> None:
        self._body.select_song_at(index)
        self.set_is_playing(True)

    def __play_song_from_menu_at(self, index: int) -> None:
        self._music_player.play_song_at(index)
        self.set_is_playing(True)

    def __go_to_song_that_title_start_with(self, title: str) -> int:
        return self.__playlist.get_songs().find_nearest_song_index_by_title(title)
