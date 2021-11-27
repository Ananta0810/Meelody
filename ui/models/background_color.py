from sys import path

path.append(".")

from models.color import Color


class BackgroundColor:
    def __init__(self, normal: Color, hover: Color = None):
        self.normal = normal
        self.hover = hover
