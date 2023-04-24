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
    __playlists: list[PlaylistInformation]
    __player: AudioPlayer = AudioPlayer()

    def __init__(self) -> None:
        super().__init__()
        self.connect_signals()
        self.set_is_playing(False)

    @override
    def connect_signals(self) -> None:
        self._music_player.set_onclick_play(lambda index: self.play_song_from_player_at(index))
        self._music_player.set_onclick_pause(lambda index: self.set_is_playing(False))
        self._music_player.set_onclick_shuffle(lambda: self._body.refresh_menu())
        self._music_player.set_onclick_love(lambda song: self.love_song_from_player(song))

        self._body.set_onclick_play(lambda index: self.play_song_from_menu_at(index))
        self._body.set_onclick_love(lambda index: self.love_song_from_menu(index))
        self._body.set_on_keypress(lambda key: self.go_to_song_that_title_start_with(key))
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

    def load_playlists(self, playlists: list[PlaylistInformation]) -> None:
        self.__playlists = playlists
        for playlist in playlists:
            playlist.cover = playlist.cover or Images.DEFAULT_PLAYLIST_COVER
            playlist = PlaylistCardData(playlist, onclick=None)
            playlist.set_ondelete(lambda: self.__delete_playlist(playlist))
            playlist.set_onchange_title(lambda title: self.__update_playlist_name(playlist, title))
            self._body.add_playlist(playlist)

    def __choose_library(self) -> None:
        self.__load_playlist(self.__library)

    def __choose_favourites(self) -> None:
        favourite_songs: list[Song] = list(filter(lambda song: song.is_loved(), self.__library.get_songs().get_songs()))
        playlist = Playlist.create(name="Favourites", songs=PlaylistSongs(favourite_songs))
        self.__load_playlist(playlist)

    def __create_empty_playlist(self) -> None:
        content = PlaylistInformation(name="Untitled", cover=Images.DEFAULT_PLAYLIST_COVER)
        playlist = PlaylistCardData(content, onclick=None)
        playlist.set_ondelete(lambda: self._body.delete_playlist(playlist))
        playlist.set_onchange_title(lambda title: self.__update_playlist_name(playlist, title))

        self._body.add_playlist(playlist)
        self.__playlists.append(playlist.content)
        LibraryHelper.save_playlists(self.__playlists)

    def __update_playlist_name(self, playlist: PlaylistCardData, title: str) -> None:
        playlist.content.name = title
        LibraryHelper.save_playlists(self.__playlists)

    def __delete_playlist(self, playlist: PlaylistCardData) -> None:
        self._body.delete_playlist(playlist)
        self.__playlists.remove(playlist.content)
        LibraryHelper.save_playlists(self.__playlists)

    def __load_playlist(self, playlist: Playlist) -> None:
        self.__playlist = playlist
        self._music_player.load_playlist_songs(playlist.get_songs())
        self._body.load_playlist(playlist)

    def love_song_at(self, index: int) -> None:
        if self.__player.get_current_song_index() == index:
            self._music_player.change_love_state()
            return
        song = self.__playlist.get_songs().get_song_at(index)
        song.reverse_love_state()

    def love_song_from_player(self, song: Song) -> None:
        self._body.love_song(song.is_loved())
        LibraryHelper.update_love_state_of(song)

    def love_song_from_menu(self, index: int) -> None:
        self.love_song_at(index)
        LibraryHelper.update_love_state_of(self.__player.get_songs()[index])

    def play_song_from_player_at(self, index: int) -> None:
        self._body.select_song_at(index)
        self.set_is_playing(True)

    def play_song_from_menu_at(self, index: int) -> None:
        self._music_player.play_song_at(index)
        self.set_is_playing(True)

    def go_to_song_that_title_start_with(self, title: str) -> int:
        return self.__playlist.get_songs().find_nearest_song_index_by_title(title)
