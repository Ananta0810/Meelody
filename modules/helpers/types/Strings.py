import os
import re
import string
from locale import setlocale, LC_ALL

setlocale(LC_ALL, "")


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


def clean_name(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9 ]+", "", unaccent(value))


def compare(text: str, other: str) -> int:
    text = unaccent(text)
    other = unaccent(other)
    if text < other:
        return -1
    if text > other:
        return 1
    return 0


def equals(text: str, other: str) -> bool:
    return compare(text, other) == 0


def unindent(value: str):
    return '\n'.join(map(str.lstrip, [line for line in value.splitlines() if line != "\n"]))


def unindent_multiple_lines(value: str):
    indent_: str = (next(i for i, j in enumerate(value) if j not in string.whitespace) - 1) * ' '
    lines = [line.replace(indent_, '') for line in value.splitlines() if line != ""]
    return '\n'.join(lines)


def indent(value: str, level: int = 1):
    indent_: str = '\n' + '    ' * level
    return indent_.join(map(str.lstrip, value.splitlines()))


def get_full_path(directory: str, name: str, extension: str) -> str:
    return "".join([directory, "/", name, extension])


def get_filename(file_path: str) -> str:
    return file_path.split("/")[-1]


def join_path(directory: str, file_path: str) -> str:
    return f"{directory}/{file_path}"


def get_dir_from(file_path: str) -> str:
    return file_path.replace(os.path.basename(file_path), "")


def get_file_basename(file_path: str) -> str:
    parts = os.path.basename(file_path).split(".")
    size = len(parts)
    if size == 0:
        return ""
    return ".".join(parts[:size - 1])


def extension_of(file_path: str) -> str:
    return os.path.basename(file_path).split(".")[1]


def rename_file(file_path: str, new_base_name: str) -> str:
    old_base_name = get_file_basename(file_path)
    if old_base_name.strip() == "":
        directory = get_dir_from(file_path)
        extension = "." + extension_of(file_path)
        return get_full_path(directory, new_base_name, extension)

    return file_path.replace(old_base_name, new_base_name)
