from models.color import Color


class BackgroundColor:
    def __init__(self, normal: Color, hover: Color):
        self.normal = normal
        self.hover = hover
