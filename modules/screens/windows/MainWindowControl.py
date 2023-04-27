from modules.helpers import DataSaver
from modules.helpers.types.Bytes import Bytes, BytesModifier
from modules.helpers.types.Decorators import override
from modules.helpers.types.Lists import Lists
from modules.models.AppSettings import AppSettings
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
    __settings: AppSettings = None
    __playlists: list[Playlist] = []
    __player: AudioPlayer = AudioPlayer()
    __selecting_playlist_songs: set[int] = set()
    __is_selecting_library: bool = False

    def __init__(self) -> None:
        super().__init__()
        self._set_default_playlist_cover(Images.DEFAULT_PLAYLIST_COVER)
        self.connect_signals()
        self.set_is_playing(False)

    @override
    def connect_signals(self) -> None:
        self._music_player.set_onclick_next(lambda index: self.__disable_edit_song_at(index))
        self._music_player.set_onclick_prev(lambda index: self.__disable_edit_song_at(index))
        self._music_player.set_onclick_play(lambda index: self.__play_song_from_player_at(index))
        self._music_player.set_onclick_pause(lambda index: self.set_is_playing(False))
        self._music_player.set_onclick_shuffle(lambda shuffled: self.__shuffle(shuffled))
        self._music_player.set_onclick_loop(lambda looping: self.__loop(looping))
        self._music_player.set_onclick_love(lambda song: self.__love_song_from_player(song))

        self._body.set_onclick_play(lambda index: self.__play_song_from_menu_at(index))
        self._body.set_onclick_love(lambda index: self.__love_song_from_menu(index))
        self._body.set_onclick_add_to_playlist(lambda index: self.__add_song_from_menu_at(index))
        self._body.set_onclick_remove_from_playlist(lambda index: self.__remove_song_from_menu_at(index))
        self._body.set_on_change_song_cover(lambda index, path: self.__change_cover_for_song_at(index, path))
        self._body.set_onchange_song_title(lambda index, title: self.__change_title_for_song_at(index, title))
        self._body.set_onclick_select_songs_fn(lambda: self.__start_select_songs_from_library_to_playlist())
        self._body.set_onclick_apply_select_songs_fn(lambda: self.__finish_select_songs_from_library_to_playlist())
        self._body.set_on_keypress(lambda key: self.__go_to_song_that_title_start_with(key))

        self._body.set_onclick_library(self.__choose_library)
        self._body.set_onclick_favourites(self.__choose_favourites)
        self._body.set_onclick_add_playlist(self.__create_empty_playlist)

        self.set_onclick_close(lambda: self._music_player.pause_current_song())
        self.set_onclick_play_on_tray(lambda: self._music_player.play_current_song())
        self.set_onclick_pause_on_tray(lambda: self._music_player.pause_current_song())
        self.set_onclick_prev_on_tray(lambda: self.play_previous_song())
        self.set_onclick_next_on_tray(lambda: self.play_next_song())

    def play_previous_song(self) -> None:
        self._music_player.play_previous_song()
        if self.__is_selecting_library:
            self.__disable_edit_song_at(self.__player.get_current_song_index())

    def play_next_song(self) -> None:
        self._music_player.play_next_song()
        if self.__is_selecting_library:
            self.__disable_edit_song_at(self.__player.get_current_song_index())

    def set_appsettings(self, settings: AppSettings) -> None:
        self.__settings = settings

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
        self._body.enable_edit_songs(True)
        self.__is_selecting_library = True
        song = self.__player.get_current_song()
        if song is not None:
            index = self.__library.get_songs().index_of(song)
            self._body.enable_edit_of_song_at(index, False)

    def __choose_favourites(self) -> None:
        self._body.enable_choosing_song(False)
        self._body.enable_add_new_song(False)

        favourite_songs: list[Song] = list(filter(lambda song: song.is_loved(), self.__library.get_songs().get_songs()))
        playlist = Playlist.create(name="Favourites",
                                   songs=PlaylistSongs(favourite_songs),
                                   cover=Images.FAVOURITES_PLAYLIST_COVER)
        self.__select_playlist(playlist)
        self._body.enable_edit_songs(False)
        self.__is_selecting_library = False

    def __choose_playlist(self, playlist: Playlist) -> None:
        self._body.enable_choosing_song(False)
        self._body.enable_add_new_song(True)
        self.__select_playlist(playlist)
        self._body.enable_edit_songs(False)
        self.__is_selecting_library = False

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
        DataSaver.save_playlists(self.__playlists)

    def __update_playlist_cover(self, card: PlaylistCardData, cover_path: str) -> None:
        card.content().cover = Bytes.get_bytes_from_file(cover_path)
        self._body.update_playlist(card)
        self.__update_display_playlist_info_if_updating(card)
        DataSaver.save_playlists(self.__playlists)

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

        DataSaver.save_playlists(self.__playlists)

    def __show_library_on_menu_and_player(self):
        self.__apply_settings_to_music_player_and_menu()
        self.__choose_library()
        self._music_player.load_playlist_songs(self.__displaying_playlist.get_songs())
        song_index = Lists.index_of(
            condition=lambda song: song.get_id() == self.__settings.playing_song_id,
            collection=self.__displaying_playlist.get_songs().get_songs(),
            index_if_not_found=0
        )
        self._music_player.load_playing_song(song_index)
        self._body.enable_edit_of_song_at(song_index, False)

    def __apply_settings_to_music_player_and_menu(self):
        self._music_player.set_shuffle(self.__settings.is_shuffle)
        self._music_player.set_loop(self.__settings.is_looping)
        if self.__settings.is_shuffle:
            self.__library.get_songs().shuffle()

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
        DataSaver.save_playlists(self.__playlists)
        self.__choose_playlist(self.__displaying_playlist)

    def __add_song_from_menu_at(self, index: int) -> None:
        self.__selecting_playlist_songs.add(index)

    def __remove_song_from_menu_at(self, index: int) -> None:
        self.__selecting_playlist_songs.remove(index)

    def __change_cover_for_song_at(self, index: int, path: str) -> None:
        bytes_data = BytesModifier \
            .of(Bytes.get_bytes_from_file(path)) \
            .square() \
            .resize(256, 256) \
            .to_bytes()
        song = self.__displaying_playlist.get_songs().get_song_at(index)
        song.set_cover(bytes_data)
        self.__choose_library()
        DataSaver.save_songs(self.__library.get_songs().get_songs())

    def __change_title_for_song_at(self, index: int, new_title: str) -> bool:
        old_song = self.__displaying_playlist.get_songs().get_song_at(index)
        new_song = old_song.clone()
        change_successfully = new_song.set_title(new_title)
        # TODO: Show alert box here.
        if not change_successfully:
            return False

        self.__library.get_songs().remove_song(old_song)
        self.__library.get_songs().insert(new_song)
        self.__choose_library()
        DataSaver.save_songs(self.__library.get_songs().get_songs())
        return True

    def __love_song_from_player(self, song: Song) -> None:
        self._body.love_song(song.is_loved())
        DataSaver.update_love_state_of(song)

    def __love_song_from_menu(self, index: int) -> None:
        if self.__player.get_current_song_index() == index:
            self._music_player.change_love_state()
            return
        song = self.__displaying_playlist.get_songs().get_song_at(index)
        song.reverse_love_state()
        DataSaver.update_love_state_of(self.__player.get_songs()[index])

    def __play_song_from_player_at(self, index: int) -> None:
        if self.__playing_playlist is None:
            self.__playing_playlist = self.__displaying_playlist

        self._body.select_song_at(index)
        self.set_is_playing(True)
        self._body.enable_edit_of_song_at(index, False)

        self.__settings.set_playing_song_id(self.__song_at(index).get_id())
        DataSaver.save_settings(self.__settings)

    def __play_song_from_menu_at(self, index: int) -> None:
        self.__playing_playlist = self.__displaying_playlist

        self._music_player.load_playlist_songs(self.__displaying_playlist.get_songs())
        self._music_player.play_song_at(index)
        self.set_is_playing(True)
        self.__disable_edit_song_at(index)

        self.__settings.set_playing_song_id(self.__song_at(index).get_id())
        DataSaver.save_settings(self.__settings)

    def __disable_edit_song_at(self, index):
        if self.__is_selecting_library:
            total = range(0, self.__library.get_songs().size())
            for index_ in total:
                self._body.enable_edit_of_song_at(index_, True)
            self._body.enable_edit_of_song_at(index, False)

    def __shuffle(self, shuffled: bool) -> None:
        self._body.refresh_menu()
        self.__settings.set_is_shuffle(shuffled)
        DataSaver.save_settings(self.__settings)

    def __loop(self, looping: bool) -> None:
        self.__settings.set_is_looping(looping)
        DataSaver.save_settings(self.__settings)

    def __go_to_song_that_title_start_with(self, title: str) -> int:
        return self.__displaying_playlist.get_songs().find_nearest_song_index_by_title(title)

    def __song_at(self, index: int) -> Song:
        return self.__playing_playlist.get_songs().get_song_at(index)
