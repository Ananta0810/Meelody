import json
from json import JSONDecodeError
from typing import final

from app.common.exceptions import StorageException
from app.helpers.base import Strings
from .files import Files
from .logger import Logger


@final
class Jsons:

    @staticmethod
    def updateToFile(jsonFile: str, key: str, value: str) -> None:
        with open(jsonFile, "r+") as jsonFile:
            data = json.load(jsonFile)

            data[key] = value

            jsonFile.seek(0)
            json.dump(data, jsonFile, indent=4)
            jsonFile.truncate()

    @staticmethod
    def jsonOf(obj: any) -> str:
        return json.dumps(obj)

    @staticmethod
    def writeToFile(file: str, obj: any) -> None:
        if not file.endswith(".json"):
            raise IOError("File should ends with json.")

        directory = Strings.getDirectoryOf(file)
        Files.createDirectoryIfNotExisted(directory)

        oldContent = Jsons.readFromFile(file)
        try:
            with open(file, 'w+') as outfile:
                newContent: str = json.dumps(obj)
                outfile.write(newContent)
        except TypeError:
            Logger.error("New content is invalid. Revert old content now.")
            if oldContent is not None:
                with open(file, 'w+') as outfile:
                    newContent: str = json.dumps(oldContent)
                    outfile.write(newContent)
            raise StorageException("Save data failed.")

    @staticmethod
    def readFromFile(file: str) -> any:
        if not file.endswith(".json"):
            raise IOError("File should ends with json.")

        try:
            with open(file) as jsonFile:
                try:
                    return json.load(jsonFile)
                except JSONDecodeError:
                    return None
        except FileNotFoundError:
            return None
