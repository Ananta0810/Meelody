import uuid

from modules.helpers.types.Strings import Strings


class PlaylistInformation:
    def __init__(self, name: str = None, cover: bytes = None):
        self.name: str = name
        self.cover: bytes = cover
        self.id: str = str(uuid.uuid4())

    def __eq__(self, other: 'PlaylistInformation') -> bool:
        return Strings.equals(self.name, other.name) and self.cover == other.cover

    def isNull(self) -> bool:
        return self.name is None

    @staticmethod
    def from_json(json: dict) -> 'PlaylistInformation':
        playlist = PlaylistInformation()
        for key in json.keys():
            playlist.__dict__[key] = json[key]

        return playlist
