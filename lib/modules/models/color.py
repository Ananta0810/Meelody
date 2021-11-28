class Color:
    red: int
    green: int
    blue: int
    alpha: float

    def __init__(self, red: int, green: int, blue: int, alpha: float = 1.0):
        self.red = red
        self.green = green
        self.blue = blue
        self.alpha = alpha

    def __str__(self):
        return f"rgba({self.red}, {self.green}, {self.blue}, {self.alpha})"

    def withAlpha(self, alpha: float):
        return Color(self.red, self.green, self.blue, alpha)
