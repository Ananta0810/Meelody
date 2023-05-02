import shutil
import tempfile
from threading import Thread
from time import sleep

from PyQt5.QtCore import pyqtSignal

from modules.helpers import Files, Times, Printers
from modules.helpers.Database import Database
from modules.helpers.Youtubes import YoutubeDownloader
from modules.helpers.types.Bytes import Bytes, BytesModifier
from modules.helpers.types.Decorators import override
from modules.helpers.types import Lists, Strings
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
from modules.widgets.Dialogs import Dialogs


class MainWindowControl(MainWindowView, BaseControl):
    __library: Playlist
    __displaying_playlist: Playlist = None
    __playing_playlist: Playlist = None
    __settings: AppSettings = None
    __playlists: list[Playlist] = []
    __player: AudioPlayer = AudioPlayer()
    __selecting_playlist_songs: set[int] = set()
    __is_selecting_library: bool = False
    __start_download: pyqtSignal = pyqtSignal()
    __downloaders: list[YoutubeDownloader] = []
    __download_thread: Thread | None = None

    def __init__(self) -> None:
        super(MainWindowControl, self).__init__()
        self._set_default_playlist_cover(Images.DEFAULT_PLAYLIST_COVER)
        self.connect_signals()
        self.set_is_playing(False)

    @override
    def connect_signals(self) -> None:
        self._music_player.set_onclick_next(lambda index: self.__disable_edit_and_delete_on_libray_of_song_at(index))
        self._music_player.set_onclick_prev(lambda index: self.__disable_edit_and_delete_on_libray_of_song_at(index))
        self._music_player.set_onclick_play(lambda index: self.__play_song_from_player_at(index))
        self._music_player.set_onclick_pause(lambda index: self.set_is_playing(False))
        self._music_player.set_onclick_shuffle(lambda shuffled: self.__shuffle(shuffled))
        self._music_player.set_onclick_loop(lambda looping: self.__loop(looping))
        self._music_player.set_onclick_love(lambda song: self.__love_song_from_player(song))

        self._body.set_onclick_play(lambda index: self.__play_song_from_menu_at(index))
        self._body.set_onclick_love(lambda index: self.__love_song_from_menu(index))
        self._body.set_onclick_add_to_playlist(lambda index: self.__add_song_from_menu_at(index))
        self._body.set_onclick_remove_from_playlist(lambda index: self.__remove_song_from_menu_at(index))
        self._body.set_onchange_song_title_and_artist_on_menu(
            lambda index, title, artist: self.__change_title_and_title_for_song_at(index, title, artist))
        self._body.set_on_change_song_cover_on_menu(lambda index, path: self.__change_cover_for_song_at(index, path))
        self._body.set_on_delete_song_on_menu(lambda index: self.__delete_song_at(index))
        self._body.set_onclick_download_songs_to_library_fn(
            lambda youtube_url: self.__add_songs_to_library_from_youtube(youtube_url)
        )
        self._body.set_onclose_download_dialog(lambda: self.__on_close_download_dialog())
        self._body.set_onclick_add_songs_to_library_fn(lambda paths: self.__add_songs_to_library_from_computer(paths))
        self._body.set_onclick_select_songs_to_playlist_fn(lambda: self.__start_select_songs_from_library_to_playlist())
        self._body.set_onclick_apply_select_songs_to_playlist_fn(
            lambda: self.__finish_select_songs_from_library_to_playlist())
        self._body.set_on_keypress(lambda key: self.__go_to_song_that_title_start_with(key))

        self._body.set_onclick_library(self.__choose_library)
        self._body.set_onclick_favourites(self.__choose_favourites)
        self._body.set_onclick_add_playlist(self.__create_empty_playlist)

        self.set_on_exit(lambda: self._music_player.pause_current_song())
        self.set_onclick_play_on_tray(lambda: self._music_player.play_current_song())
        self.set_onclick_pause_on_tray(lambda: self._music_player.pause_current_song())
        self.set_onclick_prev_on_tray(lambda: self.play_previous_song())
        self.set_onclick_next_on_tray(lambda: self.play_next_song())

        self.__start_download.connect(lambda: self._body.add_download_item(Lists.last_of(self.__downloaders).get_video_title()))

    def play_previous_song(self) -> None:
        self._music_player.play_previous_song()
        if self.__is_selecting_library:
            self.__disable_edit_and_delete_on_libray_of_song_at(self.__player.get_current_song_index())

    def play_next_song(self) -> None:
        self._music_player.play_next_song()
        if self.__is_selecting_library:
            self.__disable_edit_and_delete_on_libray_of_song_at(self.__player.get_current_song_index())

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
        self.__select_playlist(self.__library)

        self.__is_selecting_library = True
        self._body.enable_add_songs_to_library(True)
        self._body.enable_download_songs_to_library(True)
        self._body.enable_select_songs_to_playlist(False)
        self._body.enable_choosing_song(False)
        self._body.enable_edit_songs(True)
        self._body.enable_delete_songs(True)

        song = self.__player.get_current_song()
        if song is not None:
            displaying_song_index = self.__library.get_songs().index_of(song)
            self._body.enable_edit_of_song_at(displaying_song_index, False)
            self._body.enable_delete_song_at(displaying_song_index, False)

    def __choose_favourites(self) -> None:
        favourite_songs: list[Song] = list(filter(lambda song: song.is_loved(), self.__library.get_songs().get_songs()))
        playlist = Playlist.create(name="Favourites",
                                   songs=PlaylistSongs(favourite_songs),
                                   cover=Images.FAVOURITES_PLAYLIST_COVER)
        self.__select_playlist(playlist)

        self.__is_selecting_library = False
        self._body.enable_add_songs_to_library(False)
        self._body.enable_download_songs_to_library(False)
        self._body.enable_select_songs_to_playlist(False)
        self._body.enable_choosing_song(False)
        self._body.enable_edit_songs(False)
        self._body.enable_delete_songs(False)

    def __choose_playlist(self, playlist: Playlist) -> None:
        self.__select_playlist(playlist)

        self.__is_selecting_library = False
        self._body.enable_add_songs_to_library(False)
        self._body.enable_download_songs_to_library(False)
        self._body.enable_select_songs_to_playlist(True)
        self._body.enable_choosing_song(True)
        self._body.enable_edit_songs(False)
        self._body.enable_delete_songs(True)

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
        Database().playlists.save(self.__playlists)

    def __update_playlist_cover(self, card: PlaylistCardData, cover_path: str) -> None:
        card.content().cover = Bytes.get_bytes_from_file(cover_path)
        self._body.update_playlist(card)
        self.__update_display_playlist_info_if_updating(card)
        Database().playlists.save(self.__playlists)

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

        Database().playlists.save(self.__playlists)

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
        if self.__library.get_songs().has_any_song():
            self._body.enable_edit_of_song_at(song_index, False)
            self._body.enable_delete_song_at(song_index, False)

    def __apply_settings_to_music_player_and_menu(self):
        self._music_player.set_shuffle(self.__settings.is_shuffle)
        self._music_player.set_loop(self.__settings.is_looping)
        if self.__settings.is_shuffle:
            self.__library.get_songs().shuffle()

    def find_playlist_of(self, card: PlaylistCardData) -> Playlist:
        return next(playlist_ for playlist_ in self.__playlists if playlist_.get_info().id == card.content().id)

    def __add_songs_to_library_from_computer(self, paths: list[str]) -> None:
        new_songs = self.__add_songs_to_library(paths)
        if len(new_songs) == 0:
            return
        if self.__is_selecting_library:
            self.__choose_library()
        for song in new_songs:
            print(f"Inserted song {song.get_title()} to library.")

    def __add_songs_to_library_from_youtube(self, youtube_url: str) -> None:
        if youtube_url is None or youtube_url.strip() == "":
            Dialogs.alert(
                image=Images.WARNING,
                header="Warning",
                message=f"Please enter Youtube url to download song."
            )
            return

        Thread(target=lambda: self.__download_song(youtube_url)).start()

    def __download_song(self, youtube_url: str) -> None:
        try:
            downloader = YoutubeDownloader(youtube_url)

            downloader.extract_info()
            self.__validate_youtube_url(downloader)
            self.__downloaders.append(downloader)
            self.__start_download.emit()

            download_temp_dir = tempfile.mkdtemp()
            downloader.on_succeed(lambda path: self.__download_song_succeed(downloader, download_temp_dir))
            downloader.on_failed(lambda error: self.__download_song_failed(downloader, error))

            print(f"Downloading song from youtube with url '{youtube_url}'")
            downloader.download_to(download_temp_dir)
        except ValueError as e:
            Dialogs.alert(image=Images.WARNING, header="Warning", message=str(e))

        if self.__download_thread is None:
            self.__download_thread = Thread(target=lambda: self.__update_progress_items())
            self.__download_thread.start()

    def __download_song_failed(self, downloader: YoutubeDownloader, error: str) -> None:
        Printers.error(f"Download '{downloader.get_video_title()}' failed")
        Dialogs.alert(image=Images.WARNING, header="Warning", message=error)
        index = self.__downloaders.index(downloader)
        self._body.mark_failed_download_at(index)

    def __update_progress_items(self) -> None:
        active_downloaders = {downloader
                              for downloader in self.__downloaders if
                              downloader.is_downloading() or downloader.is_processing()}

        while len(active_downloaders) > 0:
            for index, downloader in enumerate(self.__downloaders):
                if downloader in active_downloaders:
                    if downloader.is_downloading():
                        self.__show_download_progress(index, downloader)
                    else:
                        self.__show_process_progress(index)
            sleep(0.05)
            active_downloaders = {downloader for downloader in self.__downloaders if
                                  downloader.is_downloading() or downloader.is_processing()}

        self.__download_thread = None

    def __validate_youtube_url(self, downloader: YoutubeDownloader) -> None:
        youtube_title = downloader.get_video_title()

        existing_song_titles = {song.get_title() for song in self.__library.get_songs().get_songs()}
        if youtube_title in existing_song_titles:
            raise ValueError("You already have this song.")

        downloading_song_titles = {downloader_.get_video_title() for downloader_ in self.__downloaders}
        if youtube_title in downloading_song_titles:
            raise ValueError("You are downloading this youtube video.")

    def __show_download_progress(self, index: int, downloader: YoutubeDownloader) -> None:
        try:
            percentage = downloader.get_percentage()
            download_size = round(downloader.get_downloaded_size() / 1000000, 2)
            total_size = round(downloader.get_size() / 1000000, 2)
            remain_sec = Times.string_of(float(downloader.get_remain_seconds()))
            description = f"{percentage}%   |   {download_size}/{total_size}MB   |  estimate: {remain_sec}"
            self._body.set_description_in_download_dialog_at(index, description)
            self._body.set_progress_in_download_dialog_at(index, percentage)
        except IndexError:
            pass

    def __show_process_progress(self, index: int) -> None:
        try:
            self._body.mark_processing_download_at(index)
        except IndexError:
            pass

    def __download_song_succeed(self, downloader: YoutubeDownloader, download_temp_dir: str) -> None:
        print(f"Downloaded song from youtube successfully with title '{downloader.get_video_title()}'.")

        download_files = Files.get_files_from(download_temp_dir, with_extension="mp3")
        song = self.__add_songs_to_library(download_files)[0]
        shutil.rmtree(download_temp_dir)

        self._body.mark_succeed_download_at(self.__downloaders.index(downloader))
        Dialogs.alert(
            image=Images.DOWNLOAD,
            header="Download successfully",
            message=f"Your video with title '{song.get_title()}' has been downloaded successfully."
        )

        if not self._body.is_opening_download_dialog():
            self.__on_close_download_dialog()

    def __on_close_download_dialog(self) -> None:
        if self.__is_selecting_library:
            self.__choose_library()

    def __add_songs_to_library(self, paths: list[str] | set[str]) -> list[Song]:
        new_songs: list[Song] = []
        for path in paths:
            print(f"Adding song from path '{path}'")
            try:
                song_path = Files.copy_file(path, "library/")
                song = Song.from_file(song_path)
                new_songs.append(song)
            except FileExistsError:
                Printers.error(f"Copy failed for {path}")
                pass

        if len(new_songs) == 0:
            return []

        self.__library.get_songs().insertAll(new_songs)
        self.__save_library()
        return new_songs

    def __save_library(self):
        Database().songs.save(self.__library.get_songs().get_songs())

    @staticmethod
    def __add_songs_from_path(paths):
        new_songs: list[Song] = []
        for path in paths:
            try:
                song_path = Files.copy_file(path, "library/")
                song = Song.from_file(song_path)
                new_songs.append(song)
            except FileExistsError:
                pass
        return new_songs

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

        temp_playlist: Playlist = Playlist(info=self.__displaying_playlist.get_info(), songs=PlaylistSongs(temp_songs))

        self._body.load_choosing_playlist(temp_playlist)

    def __finish_select_songs_from_library_to_playlist(self) -> None:
        playlist_songs = [song for index, song in enumerate(self.__library.get_songs().get_songs()) if
                          index in self.__selecting_playlist_songs]
        self.__selecting_playlist_songs.clear()

        self.__displaying_playlist.get_songs().get_songs().clear()
        self.__displaying_playlist.get_songs().insertAll(playlist_songs)
        Database().playlists.save(self.__playlists)
        self.__choose_playlist(self.__displaying_playlist)

    def __add_song_from_menu_at(self, index: int) -> None:
        self.__selecting_playlist_songs.add(index)

    def __remove_song_from_menu_at(self, index: int) -> None:
        self.__selecting_playlist_songs.remove(index)

    def __change_title_and_title_for_song_at(self, index: int, new_title: str, new_artist: str) -> bool:
        old_song = self.__displaying_playlist.get_songs().get_song_at(index)
        new_song = old_song.clone()

        new_title = new_title.strip()
        new_artist = new_artist.strip()

        changed_title: bool = False
        if (old_song.get_title() or '') != new_title:
            existing_title = {song.get_title() for song in self.__library.get_songs().get_songs() if
                              song.get_title() != old_song.get_title()}
            if new_title in existing_title:
                Dialogs.alert(
                    image=Images.WARNING,
                    header="Warning",
                    message=f"Song has already existed."
                )
                return False
            changed_title = new_song.set_title(new_title.strip())

        changed_artist = self.__change_song_artist(new_artist, new_song, old_song)

        if not changed_title and not changed_artist:
            Dialogs.alert(
                image=Images.WARNING,
                header="Warning",
                message=f"Please enter new information for song."
            )
            return False

        self.__library.get_songs().remove_song(old_song)
        self.__library.get_songs().insert(new_song)
        self.__choose_library()
        self.__save_library()

        Dialogs.alert(
            image=Images.EDIT,
            header="Edit song successfully",
            message=f"You have successfully change information for song '{new_song.get_title()}'."
        )
        return True

    @staticmethod
    def __change_song_title(new_song, new_title, old_song) -> bool | None:
        if (old_song.get_title() or '') != new_title:
            return new_song.set_title(new_title)
        return None

    @staticmethod
    def __change_song_artist(new_artist, new_song, old_song) -> bool | None:
        if (old_song.get_artist() or '') != new_artist:
            return new_song.set_artist(new_artist.strip())
        return None

    def __change_cover_for_song_at(self, index: int, path: str) -> None:
        bytes_data = BytesModifier \
            .of(Bytes.get_bytes_from_file(path)) \
            .square() \
            .resize(256, 256) \
            .to_bytes()
        song = self.__displaying_playlist.get_songs().get_song_at(index)
        song.set_cover(bytes_data)
        self.__choose_library()
        self.__save_library()

    def __delete_song_at(self, index: int) -> None:
        song = self.__displaying_playlist.get_songs().get_song_at(index)

        if self.__is_selecting_library:
            song.delete()
            self.__library.get_songs().remove_song(song)
            self.__choose_library()
            self.__save_library()
            return

        self.__displaying_playlist.get_songs().remove_song(song)
        self.__choose_playlist(self.__displaying_playlist)
        Database().playlists.save(self.__playlists)

    def __love_song_from_player(self, song: Song) -> None:
        self._body.love_song(song.is_loved())
        self.__save_library()

    def __love_song_from_menu(self, index: int) -> None:
        if self.__player.get_current_song_index() == index:
            self._music_player.change_love_state()
            return
        song = self.__displaying_playlist.get_songs().get_song_at(index)
        song.reverse_love_state()
        self.__save_library()

    def __play_song_from_player_at(self, index: int) -> None:
        if self.__playing_playlist is None:
            self.__playing_playlist = self.__displaying_playlist

        self._body.select_song_at(index)
        self.set_is_playing(True)
        self.__disable_edit_and_delete_on_libray_of_song_at(index)

        self.__settings.set_playing_song_id(self.__song_at(index).get_id())
        Database().settings.save(self.__settings)

    def __play_song_from_menu_at(self, index: int) -> None:
        self.__playing_playlist = self.__displaying_playlist

        self._music_player.load_playlist_songs(self.__displaying_playlist.get_songs())
        self._music_player.play_song_at(index)
        self.set_is_playing(True)
        self.__disable_edit_and_delete_on_libray_of_song_at(index)

        self.__settings.set_playing_song_id(self.__song_at(index).get_id())
        Database().settings.save(self.__settings)

    def __disable_edit_and_delete_on_libray_of_song_at(self, index):
        if not self.__is_selecting_library:
            return
        self._body.enable_edit_songs(True)
        self._body.enable_delete_songs(True)
        if self.__library.get_songs().has_any_song():
            self._body.enable_edit_of_song_at(index, False)
            self._body.enable_delete_song_at(index, False)

    def __shuffle(self, shuffled: bool) -> None:
        self._body.refresh_menu()
        self.__settings.set_is_shuffle(shuffled)
        Database().settings.save(self.__settings)

    def __loop(self, looping: bool) -> None:
        self.__settings.set_is_looping(looping)
        Database().settings.save(self.__settings)

    def __go_to_song_that_title_start_with(self, title: str) -> int:
        return self.__displaying_playlist.get_songs().find_nearest_song_index_by_title(title)

    def __song_at(self, index: int) -> Song:
        return self.__playing_playlist.get_songs().get_song_at(index)
