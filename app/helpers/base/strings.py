import os
import re
import string
from locale import setlocale, LC_ALL
from random import choices
from typing import final

setlocale(LC_ALL, "")
POPULATION = string.ascii_uppercase + string.digits


@final
class Strings:

    @staticmethod
    def isBlank(value: str) -> bool:
        return value is None or value.strip() == ""

    @staticmethod
    def isNotBlank(value: str) -> bool:
        return not Strings.isBlank(value)

    @staticmethod
    def randomId() -> str:
        return str.join('', choices(POPULATION, k=13))

    @staticmethod
    def unaccent(value: str) -> str:
        if value is None:
            return ''
        value = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', value)
        value = re.sub(r'[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]', 'A', value)
        value = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', value)
        value = re.sub(r'[ÈÉẸẺẼÊỀẾỆỂỄ]', 'E', value)
        value = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', value)
        value = re.sub(r'[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]', 'O', value)
        value = re.sub(r'[ìíịỉĩ]', 'i', value)
        value = re.sub(r'[ÌÍỊỈĨ]', 'I', value)
        value = re.sub(r'[ùúụủũưừứựửữ]', 'u', value)
        value = re.sub(r'[ƯỪỨỰỬỮÙÚỤỦŨ]', 'U', value)
        value = re.sub(r'[ỳýỵỷỹ]', 'y', value)
        value = re.sub(r'[ỲÝỴỶỸ]', 'Y', value)
        value = re.sub(r'[Đ]', 'D', value)
        value = re.sub(r'[đ]', 'd', value)
        return value

    @staticmethod
    def cleanName(value: str) -> str:
        return re.sub(r"[^A-Za-z0-9 ]+", "", Strings.unaccent(value))

    @staticmethod
    def compare(text: str, other: str) -> int:
        text = Strings.unaccent(text)
        other = Strings.unaccent(other)
        if text < other:
            return -1
        if text > other:
            return 1
        return 0

    @staticmethod
    def equals(text: str, other: str) -> bool:
        return Strings.compare(text, other) == 0

    @staticmethod
    def join(separator: str, collection: list[str] | tuple[str]) -> str | None:
        if collection is None or len(collection) == 0:
            return None
        return separator.join([item for item in collection if item is not None])

    @staticmethod
    def joinStyles(collection: list[str] | tuple[str]) -> str | None:
        return Strings.join(";", collection)

    @staticmethod
    def unindent(value: str):
        return '\n'.join(map(str.lstrip, [line for line in value.splitlines() if line != "\n"]))

    @staticmethod
    def unindentMultipleLines(value: str):
        indent_: str = (next(i for i, j in enumerate(value) if j not in string.whitespace) - 1) * ' '
        lines = [line.replace(indent_, '') for line in value.splitlines() if line != ""]
        return '\n'.join(lines)

    @staticmethod
    def indent(value: str, level: int = 1):
        indent_: str = '\n' + '    ' * level
        return indent_.join(map(str.lstrip, value.splitlines()))

    @staticmethod
    def getFullPath(directory: str, name: str, extension: str) -> str:
        return "".join([directory, "/", name, extension])

    @staticmethod
    def getFilename(file_path: str) -> str:
        return file_path.split("/")[-1]

    @staticmethod
    def joinPath(directory: str, file_path: str) -> str:
        return f"{directory}/{file_path}"

    @staticmethod
    def getDirectoryOf(file_path: str) -> str:
        return file_path.replace(os.path.basename(file_path), "")

    @staticmethod
    def getFileBasename(file_path: str) -> str:
        parts = os.path.basename(file_path).split(".")
        size = len(parts)
        if size == 0:
            return ""
        return ".".join(parts[:size - 1])

    @staticmethod
    def extensionOf(file_path: str) -> str:
        return os.path.basename(file_path).split(".")[1]

    @staticmethod
    def getRenameFile(filePath: str, newBaseName: str) -> str:
        old_base_name = Strings.getFileBasename(filePath)
        if old_base_name.strip() == "":
            directory = Strings.getDirectoryOf(filePath)
            extension = "." + Strings.extensionOf(filePath)
            return Strings.getFullPath(directory, newBaseName, extension)

        return filePath.replace(old_base_name, newBaseName)

    @staticmethod
    def convertBytes(size: int):
        for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return "%3.1f %s" % (size, x)
            size /= 1024.0

        return size
