from os import path, scandir
from shutil import copyfile


class MyFile:
    @staticmethod
    def generatePath(dir: str, name: str, extension: str) -> str:
        return "".join([dir, "/", name, extension])

    @staticmethod
    def getFilename(your_path: str):
        return your_path.split("/")[-1]

    @staticmethod
    def getDirFrom(your_path: str) -> str:
        return your_path.replace(path.basename(your_path), "")

    @staticmethod
    def getFileBasename(your_path: str) -> str:
        return path.basename(your_path).split(".")[0]

    @staticmethod
    def getFileExtension(your_path: str) -> str:
        return path.splitext(your_path)[1]

    @staticmethod
    def getFilesFrom(dir: str, withExtension: str) -> list[str]:
        while dir.endswith("/"):
            dir = dir[:-1]
        files = scandir(dir)

        your_files = [
            "/".join([dir, file.name])
            for file in files
            if file.name.endswith(withExtension)
        ]
        return your_files

    @staticmethod
    def moveFile(file: str, destiny_dir: str) -> str:
        new_file_path = "/".join([destiny_dir, MyFile.get_filename(file)])
        if path.exists(new_file_path):
            return
        copyfile(file, new_file_path)
        return new_file_path
