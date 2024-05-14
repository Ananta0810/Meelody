import os

from app.common.models import Song, Playlist
from app.common.models.playlists import UserPlaylist
from app.utils.others import Jsons


class Database:
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
        self.playlists = Database._Playlists("configuration/playlists.json")


database = Database()
