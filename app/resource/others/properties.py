from typing import final


@final
class FileType:
    IMAGE: str = "JPEG, PNG (*.JPEG *.jpeg *.JPG *.jpg *.JPE *.jpe)"
    AUDIO: str = "MP3 (*.MP3 *.mp3)"


@final
class PlaylistIds:
    LIBRARY = "library"
    FAVOURITES = "favourites"
