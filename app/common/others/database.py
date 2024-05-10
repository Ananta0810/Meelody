import os

from app.common.models import Song, Playlist
from app.common.models.playlists import UserPlaylist
from app.helpers.base import Lists, Strings
from app.helpers.others import Files, Jsons


class Database:
    class _Songs:

        def __init__(self, path: str) -> None:
            self.__path = path

        def load(self, directory: str, withExtension: str) -> list[Song]:
            if not os.path.exists(directory):
                os.mkdir(directory)

            if os.path.exists(self.__path):
                data: list[dict] = Jsons.readFromFile(self.__path)
                if data is not None:
                    return [Song.fromDict(item) for item in data]

            return self.__loadSongsFromFolder(directory, withExtension)

        def __loadSongsFromFolder(self, directory, withExtension):
            files: set = Files.getFrom(directory, withExtension)
            songs = Lists.nonNull([Song.fromFile(file, Strings.getFileBasename(file)) for file in files])
            self.save(songs)
            return songs

        def save(self, songs: list[Song]) -> None:
            Jsons.writeToFile(self.__path, [song.toDict() for song in songs])

    class _Playlists:
        PATH = "configuration/playlists.json"

        def __init__(self, path: str) -> None:
            self.__path = path

        def load(self, songs: list[Song]) -> list[Playlist]:
            if os.path.exists(self.__path):
                data: list[dict] = Jsons.readFromFile(self.__path)
                if data is not None:
                    return [UserPlaylist.fromDict(item, songs) for item in data]

            self.save([])
            return []

        def save(self, data: list[UserPlaylist]) -> None:
            data = [playlist.toDict() for playlist in data]
            Jsons.writeToFile(self.__path, data)

    def __init__(self) -> None:
        self.songs = Database._Songs("configuration/songs.json")
        self.playlists = Database._Playlists("configuration/playlists.json")


database = Database()
