import os
from os import scandir
from shutil import copyfile
from typing import final

from app.helpers.base import Strings


@final
class Files:

    @staticmethod
    def getFrom(directory: str, withExtension: str) -> set[str]:
        while directory.endswith("/"):
            directory = directory[:-1]
        files = scandir(directory)

        return {Strings.joinPath(directory, file.name) for file in files if file.name.endswith(withExtension)}

    @staticmethod
    def copyFile(file: str, to_directory: str) -> str:
        destiny = "/".join([to_directory, Strings.getFilename(file)])
        if not os.path.exists(file):
            raise FileExistsError(f"{file} not found.")
        if os.path.exists(destiny):
            raise FileExistsError(f"{destiny} already existed.")
        copyfile(file, destiny)
        return destiny

    @staticmethod
    def removeFile(file: str) -> None:
        try:
            os.remove(file)
        except FileNotFoundError:
            pass
