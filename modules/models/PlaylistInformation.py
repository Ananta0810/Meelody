import uuid

from modules.helpers.types import Strings


class PlaylistInformation:
    def __init__(self, name: str = None, cover: bytes = None, id: str = None):
        self.name: str = name
        self.cover: bytes = cover
        self.id: str = id or str(uuid.uuid4())

    def __eq__(self, other: 'PlaylistInformation') -> bool:
        return Strings.equals(self.name, other.name) and self.cover == other.cover

    def isNull(self) -> bool:
        return self.name is None
