from collections import defaultdict
from functools import reduce
from typing import TypeVar, final, Callable

T = TypeVar('T')
K = TypeVar('K')


@final
class Dicts:

    @staticmethod
    def group(collection: list[T], by: Callable[[T], K]) -> dict[K, list[T]]:
        return reduce(lambda grp, val: grp[by(val)].append(val) or grp, collection, defaultdict(list))

    @staticmethod
    def mergeListOfDicts(collection: list[dict]) -> dict:
        return {k: v for dct in collection for k, v in dct.items()}
