from time import perf_counter
from typing import Callable


def measure(fn: Callable[[], None]) -> float:
    start = perf_counter()
    fn()
    end = perf_counter()
    return end - start


def string_of(time: float) -> str:
    time = int(time)
    mm = time // 60
    ss = int(time) % 60
    return ":".join([str(mm).zfill(2), str(ss).zfill(2)])
