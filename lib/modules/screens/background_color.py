from sys import path

path.append(".lib/modules/")

from modules.models.color import Color


class BackgroundColor:
    def __init__(self, normal: Color, hover: Color = None, checked: Color = None):
        self.normal = normal
        self.hover = hover
        self.checked = checked
