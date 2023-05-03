from time import perf_counter
from typing import Callable, TypeVar

T = TypeVar('T')


def measure(target: Callable[[], T], result_fn: Callable[[float], None]) -> T:
    start = perf_counter()
    result = target()
    end = perf_counter()
    result_fn(end - start)
    return result


def string_of(time: float) -> str:
    time = int(time)
    mm = time // 60
    ss = int(time) % 60
    return ":".join([str(mm).zfill(2), str(ss).zfill(2)])
