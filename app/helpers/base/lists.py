from abc import ABC
from typing import TypeVar, Generic, Callable, final

T = TypeVar('T')
R = TypeVar('R')


@final
class Lists(ABC):

    @staticmethod
    def indexOf(
        condition: Callable[[Generic[T]], bool],
        collection: list[Generic[T]],
        index_if_not_found: int = -1
    ) -> int:
        for index, item in enumerate(collection):
            if condition(item):
                return index
        return index_if_not_found

    @staticmethod
    def lastOf(collection: list[Generic[T]]) -> T | None:
        if collection is None:
            return None

        return collection[len(collection) - 1]

    @staticmethod
    def moveElement(list_: list[Generic[T]], from_index: int, to_index: int) -> None:
        start: int = from_index
        end: int = to_index
        if start == end:
            return

        list_.insert(end, list_[start])

        if start > end:
            start += 1
        list_.pop(start)

    @staticmethod
    def binarySearch(
        collection: list[Generic[T]],
        item: T,
        comparator: Callable[[T, T], int] = lambda x, y: x == y,
        nearest: bool = False
    ) -> int:
        low, high = 0, len(collection) - 1

        while low <= high:
            mid = (high + low) // 2
            element = collection[mid]
            result = comparator(item, element)
            if result == 1:
                low = mid + 1
                continue
            if result == -1:
                high = mid - 1
                continue
            return mid
        # Not found
        return low if nearest else -1

    @staticmethod
    def linearSearch(
        collection: list[T],
        item: T,
        comparator: Callable[[T, T], int] = lambda x, y: 0 if x == y else -1
    ) -> int:
        for index, element in enumerate(collection):
            if comparator(element, item) == 0:
                return index
        # Not found
        return -1

    @staticmethod
    def nearestLinearSearch(
        collection: list[T],
        item: T,
        comparator: Callable[[T, T], int] = lambda x, y: 0 if x == y else -1
    ) -> int:
        if len(collection) == 0:
            return 0

        nearest_post = 0
        last_item = list[0]
        for index, element in enumerate(collection):
            if comparator(item, element) == 0:
                return index
            if comparator(last_item, element) < 0:
                nearest_post = index
                last_item = element
        # Not found
        return nearest_post
