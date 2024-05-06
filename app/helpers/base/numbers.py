from abc import ABC
from typing import final


@final
class Numbers(ABC):

    @staticmethod
    def clamp(value: float | int, min_value: float | int, max_value: float | int) -> float | int:
        if value < min_value:
            return min_value
        if value > max_value:
            return max_value
        return value

    @staticmethod
    def randomInteger(lower: int, upper: int) -> int:
        from random import randrange
        return randrange(lower, upper + 1)
