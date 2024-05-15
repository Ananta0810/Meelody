from typing import TypeVar, Callable, final

T = TypeVar('T')
E = TypeVar('E')
R = TypeVar('R')


@final
class Lists:

    @staticmethod
    def nonNull(collection: list[E]) -> list[E]:
        if collection is None:
            return []
        return [item for item in collection if item is not None]

    @staticmethod
    def indexOf(condition: Callable[[E], bool], collection: list[E], indexIfNotFound: int = -1) -> int:
        for index, item in enumerate(collection):
            if condition(item):
                return index
        return indexIfNotFound

    @staticmethod
    def lastOf(collection: list[E]) -> T | None:
        if collection is None:
            return None

        return collection[len(collection) - 1]

    @staticmethod
    def elementAt(index: int, collection: list[E]) -> T | None:
        try:
            return collection[index]
        except IndexError:
            return None

    @staticmethod
    def elementsAfter(index: int, collection: list[E]) -> list[E]:
        try:
            return collection[index + 1:]
        except IndexError:
            return []

    @staticmethod
    def flat(collection: list[list[E]]) -> list[E]:
        import itertools
        return list(itertools.chain.from_iterable(collection))

    @staticmethod
    def clone(collection: list[E]) -> list[E]:
        return [item for item in collection]

    @staticmethod
    def shuffle(collection: list[E]) -> list[E]:
        """
        Create a shuffled list of the input collection.
        """
        import random

        return random.sample(list(Lists.clone(collection)), len(collection))

    @staticmethod
    def itemsInLeftOnly(left: list[E] | set[E], right: list[E] | set[E]) -> list[E]:
        if left is None or right is None:
            return []
        rightSet = right if isinstance(right, set) else set(right)
        return [item for item in left if item not in rightSet]

    @staticmethod
    def itemsInRightOnly(left: list[E] | set[E], right: list[E] | set[E]) -> list[E]:
        if left is None or right is None:
            return []
        leftSet = left if isinstance(left, set) else set(left)
        return [item for item in right if item not in leftSet]

    @staticmethod
    def moveElement(collection: list[E], fromIndex: int, toIndex: int) -> None:
        start: int = fromIndex
        end: int = toIndex
        if start == end:
            return

        collection.insert(end, collection[start])

        if start > end:
            start += 1
        collection.pop(start)

    @staticmethod
    def findMoved(originalList: list[E], newList: list[E]) -> (int, int):
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
    def findMostFrequency(collection: list[E]) -> T:
        return max(set(collection), key=collection.count)

    @staticmethod
    def binarySearch(
        collection: list[E],
        item: T,
        comparator: Callable[[T, E], int] = lambda x, y: x == y,
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
        collection: list[E],
        item: T,
        comparator: Callable[[T, E], int] = lambda x, y: 0 if x == y else -1
    ) -> int:
        for index, element in enumerate(collection):
            if comparator(item, element) == 0:
                return index
        # Not found
        return -1

    @staticmethod
    def nearestLinearSearch(
        collection: list[E],
        item: T,
        comparator: Callable[[T, E], int] = lambda x, y: 0 if x == y else -1
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
