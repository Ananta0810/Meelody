from PyQt5.QtCore import Qt


class Shortcut:
    __modifier: int | None = None
    __key: int | None = None

    __key_map = {Qt.__dict__[key]: key for key in Qt.__dict__ if key.startswith('Key_') or key.endswith('Modifier')}

    def __init__(self, modifier: Qt.Modifier | None = None, key: int | None = None):
        self.__modifier = 0 if modifier is None else int(modifier)
        self.__key = key or 0

    @staticmethod
    def of_key(key: int | None) -> 'Shortcut':
        return Shortcut(None, key)

    @staticmethod
    def of(modifier: Qt.Modifier, key: int) -> 'Shortcut':
        return Shortcut(modifier, key)

    def __hash__(self) -> int:
        value = hash((self.__modifier, self.__key))
        return value

    def __eq__(self, other: 'Shortcut') -> bool:
        if other is None:
            return False
        return self.__modifier == other.__modifier and self.__key == other.__key

    def __str__(self) -> str:
        shortcut = " + ".join([Shortcut.__key_map[key] for key in [self.__modifier, self.__key] if key != 0])
        return f"Shortcut:: {shortcut}"
