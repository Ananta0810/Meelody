import os

from app.common.models import Song, Playlist
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
        info = {"name": playlist.getInfo().getName(), "id": playlist.getInfo().getId()}
        ids: list[str] = [song.getId() for song in playlist.getSongs().getSongs()]

        return PlaylistJson(info=info, ids=ids)

    @staticmethod
    def fromDict(json: dict) -> 'PlaylistJson':
        return PlaylistJson(json['__info'], json['__ids'])

    def toPlaylist(self, songs: list[Song]) -> Playlist:
        ids = set(self.__ids)
        return Playlist(Playlist.Info(), Playlist.Songs(songs=[song for song in songs if song.getId() in ids]))

    def toDict(self) -> dict:
        return {
            '__info': self.__info,
            '__ids': self.__ids
        }


database = Database()
