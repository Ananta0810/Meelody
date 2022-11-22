class Numbers:
    @staticmethod
    def clamp_float(value: float, min_value: float, max_value: float) -> float:
        if value < min_value:
            return min_value
        if value > max_value:
            return max_value
        return value

    @staticmethod
    def clamp_int(value: int, min_value: int, max_value: int) -> int:
        if value < min_value:
            return min_value
        if value > max_value:
            return max_value
        return value
