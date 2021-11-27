class Border:
    def __init__(self, size: int, color, type: str = "solid"):
        self.size = size
        self.color = color
        self.type = type

    def __str__(self):
        return f"{self.size} {self.type} {self.color}"
