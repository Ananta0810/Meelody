from typing import TypeVar, Callable, final

T = TypeVar('T')
R = TypeVar('R')


@final
class Lists:

    @staticmethod
    def findMoved(originalList: list[T], newList: list[T]) -> (int, int):
        if len(originalList) != len(newList):
            return -1, -1  # different length

        diff = [x for x, (c, d) in enumerate(zip(originalList, newList)) if c != d]
        if not diff:
            return -1, -1  # equal strings
        oldIndex, newIndex = diff[0], diff[-1]

        if originalList[oldIndex + 1:newIndex + 1] == newList[oldIndex:newIndex] and originalList[oldIndex] == newList[newIndex]:
            return oldIndex, newIndex
        if originalList[oldIndex:newIndex] == newList[oldIndex + 1:newIndex + 1] and originalList[newIndex] == newList[oldIndex]:
            return newIndex, oldIndex

        return -1, -1

    @staticmethod
    def nonNull(collection: list[T]) -> list[T]:
        if collection is None:
            return []
        return [item for item in collection if item is not None]

    @staticmethod
    def indexOf(condition: Callable[[T], bool], collection: list[T], indexIfNotFound: int = -1) -> int:
        for index, item in enumerate(collection):
            if condition(item):
                return index
        return indexIfNotFound

    @staticmethod
    def lastOf(collection: list[T]) -> T | None:
        if collection is None:
            return None

        return collection[len(collection) - 1]

    @staticmethod
    def elementAt(index: int, collection: list[T]) -> T | None:
        try:
            return collection[index]
        except IndexError:
            return None

    @staticmethod
    def elementsAfter(index: int, collection: list[T]) -> list[T]:
        try:
            return collection[index + 1:]
        except IndexError:
            return []

    @staticmethod
    def moveElement(collection: list[T], fromIndex: int, toIndex: int) -> None:
        start: int = fromIndex
        end: int = toIndex
        if start == end:
            return

        collection.insert(end, collection[start])

        if start > end:
            start += 1
        collection.pop(start)

    @staticmethod
    def binarySearch(
        collection: list[T],
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

        nearestPost = 0
        lastItem = list[0]
        for index, element in enumerate(collection):
            if comparator(item, element) == 0:
                return index
            if comparator(lastItem, element) < 0:
                nearestPost = index
                lastItem = element
        # Not found
        return nearestPost
