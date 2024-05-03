from dataclasses import dataclass


@dataclass
class StorageException(Exception):
    message: str
