class Size:
    width: int
    height: int

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def __str__(self):
        return f"width: {self.width}, height: {self.height}"
