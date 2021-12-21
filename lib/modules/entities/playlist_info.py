class PlaylistInfo:
    def __init__(self, id: int = 0, name: str = None, cover: bytes = None):
        self.id = id
        self.name = name
        self.cover = cover

    def isNull(self) -> bool:
        return self.name is None
