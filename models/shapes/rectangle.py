class Rectangle:
    left: int
    top: int
    right: int
    bottom: int

    def __init__(self, left: int, top: int, right: int, bottom: int):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

    def __str__(self):
        return f'left: {self.left}, top: {self.top}, right: {self.right}, bottom: {self.bottom}'
