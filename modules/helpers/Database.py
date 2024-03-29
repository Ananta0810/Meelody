import os.path
from abc import ABC, abstractmethod

from modules.helpers import Files, Printers
from modules.helpers import Jsons
from modules.helpers.types import Strings
from modules.helpers.types.Bytes import Bytes
from modules.helpers.types.Metas import SingletonMeta
from modules.models.AppSettings import AppSettings
from modules.models.Playlist import Playlist, PlaylistJson
from modules.models.PlaylistSongs import PlaylistSongs
from modules.models.Song import Song


class DataSaver(ABC):
    _path: str = None

    def set_path(self, path: str) -> None:
        self._path = path
        directory = Strings.get_dir_from(path)
        if not os.path.exists(directory):
            os.makedirs(directory)

    def get_path(self) -> str:
        return self._path

    @abstractmethod
    def load(self, *args, **kwargs) -> ...:
        pass

    @abstractmethod
    def save(self, *args) -> None:
        pass


class Database(metaclass=SingletonMeta):
    def __init__(self):
        self.settings: SettingsSaver = SettingsSaver()
        self.songs: SongSaver = SongSaver()
        self.playlists: PlaylistSaver = PlaylistSaver()
        self.covers: CoverSaver = CoverSaver()


class SongSaver(DataSaver):

    def load(self, directory: str, with_extension: str) -> PlaylistSongs:
        return self.__get_library_songs_from_json() \
            if os.path.exists(self.get_path()) \
            else self.__get_songs_from_files(directory, with_extension)

    def save(self, data: list[Song], playing_song: Song | None) -> None:
        id_ = None if playing_song is None else playing_song.get_id()
        Jsons.write_to_file(self.get_path(), [song.to_dict(with_cover=song.get_id() == id_) for song in data])

    def __get_songs_from_files(self, directory: str, with_extension: str) -> PlaylistSongs:
        if not os.path.exists(directory):
            os.mkdir(directory)
        playlist = PlaylistSongs()
        files: set = Files.get_files_from(directory, with_extension)
        for file in files:
            playlist.insert(Song.from_file(location=file))
        self.save(playlist.get_songs(), None)
        return playlist

    def __get_library_songs_from_json(self) -> PlaylistSongs:
        playlist = PlaylistSongs()
        songs: list[dict] = Jsons.read_from_file(self.get_path()) or []
        for song in songs:
            try:
                playlist.insert(Song.from_json(song))
            except KeyError:
                Printers.error("Extract song from json failed.")
                pass
        return playlist


class CoverSaver(DataSaver):

    def load(self, songs: list[Song] = None) -> dict[str, bytes]:
        return self.__get_covers_from_json() \
            if os.path.exists(self.get_path()) \
            else self.__create_json_with_covers_of(songs or [])

    def save(self, data: list[Song]) -> None:
        file_data: list[dict[str, str]] = [self.__dict_of(song) for song in data]
        Jsons.write_to_file(self.get_path(), file_data)

    @staticmethod
    def __dict_of(song: Song) -> dict[str, str]:
        return {
            'id': song.get_id(),
            'cover': Bytes.decode(song.get_cover())
        }

    def __get_covers_from_json(self) -> dict[str, bytes]:
        data: list[dict[str, str]] = Jsons.read_from_file(self.get_path()) or {}
        return {item['id']: Bytes.encode(item['cover']) for item in data}

    def __create_json_with_covers_of(self, songs: list[Song]):
        self.save(songs)
        return {song.get_id(): song.get_cover() for song in songs}


class PlaylistSaver(DataSaver):

    def load(self, songs: list[Song]) -> list[Playlist]:
        return self.__get_library_playlists_from_json(songs) \
            if os.path.exists(self.get_path()) \
            else self.__create_empty_playlist()

    def __get_library_playlists_from_json(self, songs: list[Song]) -> list[Playlist]:
        playlists: list[dict] = Jsons.read_from_file(self.get_path()) or []
        try:
            return [PlaylistJson.from_json(playlist).to_playlist(songs) for playlist in playlists]
        except KeyError:
            Printers.error("Extract playlists from json failed.")
            return []

    def __create_empty_playlist(self) -> list[Playlist]:
        self.save([])
        return []

    def save(self, data: list[Playlist]) -> None:
        playlist_jsons: list[PlaylistJson] = [PlaylistJson.from_playlist(playlist) for playlist in data]
        data = [playlist.to_json() for playlist in playlist_jsons]
        Jsons.write_to_file(self.get_path(), data)


class SettingsSaver(DataSaver):

    def load(self) -> AppSettings:
        return self.__get_settings_from_json() \
            if os.path.exists(self.get_path()) \
            else self.__create_empty_settings()

    def __get_settings_from_json(self) -> AppSettings:
        json: dict = Jsons.read_from_file(self.get_path()) or {}
        try:
            return AppSettings.from_json(json)
        except KeyError:
            Printers.error("Extract appsettings from json failed.")
            return AppSettings()

    def __create_empty_settings(self) -> AppSettings:
        settings = AppSettings()
        self.save(settings)
        return settings

    def save(self, data: AppSettings) -> None:
        Jsons.write_to_file(self.get_path(), data.to_json())
