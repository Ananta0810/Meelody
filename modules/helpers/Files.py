import os
from os import path, scandir
from shutil import copyfile

from modules.helpers.types import Strings


def get_files_from(directory: str, with_extension: str) -> set[str]:
    while directory.endswith("/"):
        directory = directory[:-1]
    scanned_files = scandir(directory)

    return {Strings.join_path(directory, file.name) for file in scanned_files if file.name.endswith(with_extension)}


def copy_file(file: str, to_directory: str) -> str:
    destiny = "/".join([to_directory, Strings.get_filename(file)])
    if not path.exists(file):
        raise FileExistsError(f"{file} not found.")
    if path.exists(destiny):
        raise FileExistsError(f"{destiny} already existed.")
    copyfile(file, destiny)
    return destiny


def remove_file(file: str) -> None:
    try:
        os.remove(file)
    except:
        pass
