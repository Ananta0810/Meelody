from time import perf_counter
from typing import Callable, TypeVar, final

T = TypeVar('T')


@final
class Times:

    @staticmethod
    def measure(target: Callable[[], T], resultFn: Callable[[float], None]) -> T:
        start = perf_counter()
        result = target()
        end = perf_counter()
        resultFn(end - start)
        return result

    @staticmethod
    def toString(time: float) -> str:
        time = int(time)
        mm = time // 60
        ss = int(time) % 60
        return ":".join([str(mm).zfill(2), str(ss).zfill(2)])
