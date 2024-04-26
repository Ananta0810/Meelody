import os

from app.common.models import Song
from app.helpers.others import Files


class Database:
    class Playlists:
        pass

    class Songs:

        @staticmethod
        def load(directory: str, withExtension: str) -> list[Song]:
            if not os.path.exists(directory):
                os.mkdir(directory)
            files: set = Files.getFrom(directory, withExtension)
            return [Song.fromFile(file) for file in files]


database = Database()
