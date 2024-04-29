import os

from app.common.models import Song
from app.helpers.others import Files, Jsons


class Database:
    class Playlists:
        pass

    class Songs:

        PATH = "configuration/songs.json"

        @staticmethod
        def load(directory: str, withExtension: str) -> list[Song]:
            if not os.path.exists(directory):
                os.mkdir(directory)

            if os.path.exists(Database.Songs.PATH):
                data: list[dict] = Jsons.readFromFile(Database.Songs.PATH) or []
                return [Song.fromDict(item) for item in data]

            files: set = Files.getFrom(directory, withExtension)
            songs = [Song.fromFile(file) for file in files]

            Jsons.writeToFile(Database.Songs.PATH, [song.toDict() for song in songs])
            return songs


database = Database()
