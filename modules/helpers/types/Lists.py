from typing import TypeVar, Generic, Callable

from modules.helpers.types.Strings import Strings

T = TypeVar('T')
R = TypeVar('R')


class Lists:
    @staticmethod
    def move_element(list_: list[Generic[T]], from_index: int, to_index: int) -> None:
        start: int = from_index
        end: int = to_index
        if start == end:
            return

        list_.insert(end, list_[start])

        if start > end:
            start += 1
        list_.pop(start)

    @staticmethod
    def string_binary_search(
        _list: list[Generic[T]],
        search_value: str,
        key_provider: Callable[[T], str] = lambda x: x,
        find_nearest: bool = False
    ) -> int:
        low, high = 0, len(_list) - 1
        mid: int = 0
        item: T = None
        result: int = 0

        while low <= high:
            mid = (high + low) // 2
            item = _list[mid]
            result = Strings.compare(search_value, key_provider(item))
            if result == 1:
                low = mid + 1
                continue
            if result == -1:
                high = mid - 1
                continue
            return mid
        # Not found
        return low if find_nearest else -1

    @staticmethod
    def linear_search(
        _list: list[Generic[T]],
        search_item: Generic[R],
        key_provider: Callable[[T], R] = lambda x: x
    ) -> int:
        for index, item in enumerate(_list):
            if key_provider(item) == search_item:
                return index
        # Not found
        return -1

    @staticmethod
    def string_linear_search(
        _list: list[Generic[T]],
        search_value: str,
        key_provider: Callable[[T], str] = lambda x: x
    ) -> int:
        for index, item in enumerate(_list):
            if Strings.compare(search_value, key_provider(item)) == 0:
                return index
        # Not found
        return -1

    @staticmethod
    def string_nearest_linear_search(
        _list: list[Generic[T]],
        search_value: str = '',
        key_provider: Callable[[T], str] = lambda x: x
    ) -> int:
        first_letter: str = search_value[0]
        nearest_post = 0
        for index, item in enumerate(_list):
            if Strings.compare(search_value, key_provider(item)) == 0:
                return index
            if key_provider(item)[0] <= first_letter:
                nearest_post = index
        # Not found
        return nearest_post
