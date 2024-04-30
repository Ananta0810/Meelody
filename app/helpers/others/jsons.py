import json
from json import JSONDecodeError
from typing import final

from app.helpers.base import Strings
from app.helpers.others import Files


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

        with open(file, 'w+') as outfile:
            fileContent: str = json.dumps(obj, indent=4)
            outfile.write(fileContent)

    @staticmethod
    def readFromFile(file: str) -> any:
        if not file.endswith(".json"):
            raise IOError("File should ends with json.")
        with open(file) as jsonFile:
            try:
                return json.load(jsonFile)
            except JSONDecodeError:
                return None
