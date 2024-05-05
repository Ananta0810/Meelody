import io
import os
from os import scandir
from shutil import copyfile
from typing import final

from PIL import Image

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
    def copyFileToDirectory(directory: str, file: str) -> str:
        destiny = "/".join([directory, Strings.getFilename(file)])
        if not os.path.exists(file):
            raise FileNotFoundError(f"{file} not found.")
        if os.path.exists(destiny):
            raise FileExistsError(f"{destiny} already existed.")
        copyfile(file, destiny)
        return destiny

    @staticmethod
    def copyFile(file: str, destiny: str) -> None:
        if not os.path.exists(file):
            raise FileNotFoundError(f"{file} not found.")
        if os.path.exists(destiny):
            raise FileExistsError(f"{destiny} already existed.")
        copyfile(file, destiny)

    @staticmethod
    def removeFile(file: str) -> None:
        try:
            os.remove(file)
        except (FileNotFoundError, OSError):
            pass

    @staticmethod
    def createDirectoryIfNotExisted(directory):
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

    @staticmethod
    def saveImageFile(data: bytes, path: str) -> None:
        Files.createDirectoryIfNotExisted(Strings.getDirectoryOf(path))

        image = Image.open(io.BytesIO(data))
        image.save(path)
