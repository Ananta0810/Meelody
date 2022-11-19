class Numbers:
    @staticmethod
    def clampFloat(value: float, min_value: float, max_value: float) -> float:
        if value < min_value:
            return min_value
        if value > max_value:
            return max_value
        return value

    @staticmethod
    def clampInt(value: int, min_value: int, max_value: int) -> int:
        if value < min_value:
            return min_value
        if value > max_value:
            return max_value
        return value
