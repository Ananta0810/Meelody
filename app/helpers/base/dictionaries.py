from collections import defaultdict
from functools import reduce
from typing import TypeVar, final, Callable

T = TypeVar('T')
K = TypeVar('K')


@final
class Dicts:

    @staticmethod
    def getFrom(dictionary: dict[str, any], key: str, otherwise: T = None):
        return dictionary[key] if key in dictionary else otherwise

    @staticmethod
    def group(collection: list[T], by: Callable[[T], K]) -> dict[K, list[T]]:
        return reduce(lambda grp, val: grp[by(val)].append(val) or grp, collection, defaultdict(list))
