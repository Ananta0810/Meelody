import os

from app.common.models import Song, Playlist
from app.helpers.base import Bytes
from app.helpers.others import Files, Jsons


class Database:
    class _Songs:

        def __init__(self, path: str) -> None:
            self.path = path

        def load(self, directory: str, withExtension: str) -> list[Song]:
            if not os.path.exists(directory):
                os.mkdir(directory)

            if os.path.exists(self.path):
                data: list[dict] = Jsons.readFromFile(self.path) or []
                return [Song.fromDict(item) for item in data]

            return self.__loadSongsFromFolder(directory, withExtension)

        def __loadSongsFromFolder(self, directory, withExtension):
            files: set = Files.getFrom(directory, withExtension)
            songs = [Song.fromFile(file) for file in files]
            Jsons.writeToFile(self.path, [song.toDict() for song in songs])
            return songs

    class _Playlists:
        PATH = "configuration/playlists.json"

        def __init__(self, path: str) -> None:
            self.path = path

        def load(self, songs: list[Song]) -> list[Playlist]:
            if os.path.exists(self.path):
                data: list[dict] = Jsons.readFromFile(self.path) or []
                return [PlaylistJson.fromDict(item).toPlaylist(songs) for item in data]
            else:
                self.save([])
                return []

        def save(self, data: list[Playlist]) -> None:
            playlistJsons: list[PlaylistJson] = [PlaylistJson.fromPlaylist(playlist) for playlist in data]
            data = [playlist.toDict() for playlist in playlistJsons]
            Jsons.writeToFile(self.path, data)

    def __init__(self) -> None:
        self.songs = Database._Songs("configuration/songs.json")
        self.playlists = Database._Playlists("configuration/playlists.json")


class PlaylistJson:
    __info: dict
    __ids: list[str]

    def __init__(self, info: dict, ids: list[str]):
        self.__info = info
        self.__ids = ids

    @staticmethod
    def fromPlaylist(playlist: Playlist) -> 'PlaylistJson':
        playlistInfo = playlist.getInfo()

        info = {"name": playlistInfo.getName(), "id": playlistInfo.getId(), "cover": playlistInfo.getCoverPath()}
        ids: list[str] = [song.getId() for song in playlist.getSongs().getSongs()]

        return PlaylistJson(info, ids)

    @staticmethod
    def fromDict(json: dict) -> 'PlaylistJson':
        return PlaylistJson(json['info'], json['ids'])

    def toPlaylist(self, songs: list[Song]) -> Playlist:
        songIds = set(self.__ids)

        path = self.__info.get("cover", None)
        cover = None if path is None else Bytes.fromFile(path)
        path = None if cover is None else path

        info = Playlist.Info(id=self.__info["id"], name=self.__info["name"], coverPath=path, cover=cover)
        songs = Playlist.Songs(songs=[song for song in songs if song.getId() in songIds])

        return Playlist(info, songs)

    def toDict(self) -> dict:
        return {
            'info': self.__info,
            'ids': self.__ids
        }


database = Database()
