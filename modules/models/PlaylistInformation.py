from modules.helpers.types.Strings import Strings


class PlaylistInformation:
    def __init__(self, name: str = None, cover: bytes = None):
        self.name = name
        self.cover = cover

    def __eq__(self, other: 'PlaylistInformation') -> bool:
        return Strings.equals(self.name, other.name) and self.cover == other.cover

    def isNull(self) -> bool:
        return self.name is None
