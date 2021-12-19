from sys import path

from .my_string import UnicodeString

path.append("./lib")
from modules.entities.song import Song


class MyList:
    @staticmethod
    def moveElement(list_: list, from_index: int, to_index: int) -> None:
        start: int = from_index
        end: int = to_index
        if start == end:
            return

        list_.insert(end, list_[start])

        if start > end:
            start += 1
        list_.pop(start)

    @staticmethod
    def binarySearchByTitle(_list: list[Song], title: str):
        low, high = 0, len(_list) - 1
        mid: int = 0
        song: Song = None
        result: int = 0

        while low <= high:
            mid = (high + low) // 2
            song = _list[mid]
            result = UnicodeString.compare(title, song.title)
            if result == 1:
                low = mid + 1
                continue
            if result == -1:
                high = mid - 1
                continue
            return mid
        # Not found
        return -1

    @staticmethod
    def binarySearchByArtist(_list: list[Song], artist: str):
        low, high = 0, len(_list) - 1
        mid: int = 0
        song: Song = None
        result: int = 0

        while low <= high:
            mid = (high + low) // 2
            song = _list[mid]
            result = UnicodeString.compare(song.artist, artist)
            if result == 1:
                low = mid + 1
                continue
            if result == -1:
                high = mid - 1
                continue
            return mid
        # Not found
        return -1

    @staticmethod
    def linearSearch(_list: list, song) -> int:
        for index, item in enumerate(_list):
            if item == song:
                return index
        return -1

    @staticmethod
    def linearSearchByTitle(_list: list, title: str) -> int:
        for index, item in enumerate(_list):
            if item.title == title:
                return index
        return -1

    @staticmethod
    def linearSearch(_list: list, song) -> int:
        for index, item in enumerate(_list):
            if item == song:
                return index
        return -1

    @staticmethod
    def binaryInsertSearchByTitle(_list: list, title) -> int:
        low, high = 0, len(_list) - 1
        mid: int = 0
        song: Song = None
        result: int = 0

        while low <= high:
            mid = (high + low) // 2
            song = _list[mid]
            result = UnicodeString.compare(title, song.title)
            if result == 1:
                low = mid + 1
                continue
            if result == -1:
                high = mid - 1
                continue
            return mid
        # Not found
        return low
