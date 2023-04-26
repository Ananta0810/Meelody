from time import perf_counter
from typing import Callable


def measure(fn: Callable[[], None]) -> float:
    start = perf_counter()
    fn()
    end = perf_counter()
    return end - start
