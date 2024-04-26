from PyQt5.QtCore import QThread

from app.common.models import Song
from app.common.others import appCenter
from app.helpers.others import Files, Logger


class ImportSongsToLibraryThread(QThread):

    def __init__(self, songPaths: list[str]) -> None:
        super().__init__()
        self.__songPaths = songPaths

    def run(self) -> None:
        paths = self.__copySongsToLibrary()
        songs = [Song.fromFile(path) for path in paths]
        appCenter.library.getSongs().insertAll(songs)

    def __copySongsToLibrary(self) -> list[str]:
        newPaths: list[str] = []
        for path in self.__songPaths:
            try:
                songPath = Files.copyFile(path, "library/")
                print(f"Import song from '{path}' to library")
                newPaths.append(songPath)
            except FileExistsError:
                Logger.error(f"Copy failed for {path}")
                pass

        return newPaths
