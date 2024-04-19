from typing import TypeVar, final

T = TypeVar('T')


@final
class Dicts:

    @staticmethod
    def getFrom(dictionary: dict[str, any], key: str, otherwise: T = None):
        return dictionary[key] if key in dictionary else otherwise
