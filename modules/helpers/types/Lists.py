from typing import TypeVar, Generic, Callable

T = TypeVar('T')
R = TypeVar('R')


def index_of(
    condition: Callable[[Generic[T]], bool],
    collection: list[Generic[T]],
    index_if_not_found: int = -1
) -> int:
    for index, item in enumerate(collection):
        if condition(item):
            return index
    return index_if_not_found


def last_of(collection: list[Generic[T]]) -> T | None:
    if collection is None:
        return None

    return collection[len(collection) - 1]


def move_element(list_: list[Generic[T]], from_index: int, to_index: int) -> None:
    start: int = from_index
    end: int = to_index
    if start == end:
        return

    list_.insert(end, list_[start])

    if start > end:
        start += 1
    list_.pop(start)


def binary_search(
    _list: list[Generic[T]],
    search_item: T,
    comparator: Callable[[T, T], int] = lambda x, y: x == y,
    find_nearest: bool = False
) -> int:
    low, high = 0, len(_list) - 1

    while low <= high:
        mid = (high + low) // 2
        item = _list[mid]
        result = comparator(search_item, item)
        if result == 1:
            low = mid + 1
            continue
        if result == -1:
            high = mid - 1
            continue
        return mid
    # Not found
    return low if find_nearest else -1


def linear_search(
    _list: list[T],
    search_item: T,
    comparator: Callable[[T, T], int] = lambda x, y: 0 if x == y else -1
) -> int:
    for index, item in enumerate(_list):
        if comparator(item, search_item) == 0:
            return index
    # Not found
    return -1


def nearest_linear_search(
    _list: list[T],
    search_item: T,
    comparator: Callable[[T, T], int] = lambda x, y: 0 if x == y else -1
) -> int:
    if len(_list) == 0:
        return 0

    nearest_post = 0
    last_item = list[0]
    for index, item in enumerate(_list):
        if comparator(search_item, item) == 0:
            return index
        if comparator(last_item, item) < 0:
            nearest_post = index
            last_item = item
    # Not found
    return nearest_post
