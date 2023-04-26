import json
import os.path
from json import JSONDecodeError

from modules.helpers.types.Strings import Strings


class Jsons:

    @staticmethod
    def update_to_file(json_file: str, key: str, value: str) -> None:
        with open(json_file, "r+") as json_file:
            data = json.load(json_file)

            data[key] = value

            json_file.seek(0)
            json.dump(data, json_file, indent=4)
            json_file.truncate()

    @staticmethod
    def json_of(obj: any) -> str:
        return json.dumps(obj)

    @staticmethod
    def write_to_file(file: str, obj: any) -> None:
        if not file.endswith(".json"):
            raise IOError("File should ends with json.")

        directory = Strings.get_dir_from(file)
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        with open(file, 'w+') as outfile:
            file_content: str = json.dumps(obj, indent=4)
            outfile.write(file_content)

    @staticmethod
    def read_from_file(file: str) -> any:
        if not file.endswith(".json"):
            raise IOError("File should ends with json.")
        with open(file) as json_file:
            try:
                return json.load(json_file)
            except JSONDecodeError:
                return None
