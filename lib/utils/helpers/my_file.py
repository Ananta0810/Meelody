from os import path, scandir
from shutil import copyfile


class MyFile:
    @staticmethod
    def generatePath(dir: str, name: str, extension: str) -> str:
        return "".join([dir, "/", name, extension])

    @staticmethod
    def getFilename(yourPath: str):
        return yourPath.split("/")[-1]

    @staticmethod
    def getDirFrom(yourPath: str) -> str:
        return yourPath.replace(path.basename(yourPath), "")

    @staticmethod
    def getFileBasename(yourPath: str) -> str:
        return path.basename(yourPath).split(".")[0]

    @staticmethod
    def getFileExtension(yourPath: str) -> str:
        return path.splitext(yourPath)[1]

    @staticmethod
    def getFilesFrom(dir: str, withExtension: str) -> set():
        while dir.endswith("/"):
            dir = dir[:-1]
        scannedFiles = scandir(dir)
        files = set()

        for file in scannedFiles:
            if not file.name.endswith(withExtension):
                continue
            files.add("/".join([dir, file.name]))
        return files

    @staticmethod
    def moveFile(file: str, destiny_dir: str) -> str:
        new_file_path = "/".join([destiny_dir, MyFile.get_filename(file)])
        if path.exists(new_file_path):
            return
        copyfile(file, new_file_path)
        return new_file_path
