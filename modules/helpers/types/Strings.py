import os
import string
from locale import setlocale, LC_ALL

setlocale(LC_ALL, "")


def clear_non_ascii(text: str) -> str:
    if text is None:
        return ''
    return text.encode('ascii', errors='ignore').decode()


def compare(text: str, other: str) -> int:
    text = clear_non_ascii(text)
    other = clear_non_ascii(other)
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
    return os.path.basename(file_path).split(".")[0]


def extension_of(file_path: str) -> str:
    return os.path.basename(file_path).split(".")[1]


def rename_file(file_path: str, new_base_name: str) -> str:
    old_base_name = get_file_basename(file_path)
    if old_base_name.strip() == "":
        directory = get_dir_from(file_path)
        extension = "." + extension_of(file_path)
        return get_full_path(directory, new_base_name, extension)

    return file_path.replace(old_base_name, new_base_name)
