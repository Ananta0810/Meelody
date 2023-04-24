from time import perf_counter
from typing import Callable


def measure(fn: Callable[[], None], message: str) -> None:
    start = perf_counter()
    fn()
    end = perf_counter()
    print(message.format(end - start))