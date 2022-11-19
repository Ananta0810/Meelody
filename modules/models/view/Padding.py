from modules.models.view.StylesheetElement import StylesheetElement


class Padding(StylesheetElement):
    def __init__(self, width, height=None, is_relative: bool = False):
        self.width = width
        self.height = width if height is None else height
        self.is_relative = is_relative

    def getWidth(self, size: int = 0) -> float:
        if self.is_relative:
            return self.width * size
        if self.width <= 1:
            return self.width * size
        return self.width

    def getHeight(self, size: int = 0) -> float:
        if self.is_relative:
            return self.height * size
        if self.height <= 1:
            return self.height * size
        return self.height

    def to_stylesheet(self, size: int = 0) -> str:
        return f"{self.getWidth(size)}px {self.getHeight(size)}px"
