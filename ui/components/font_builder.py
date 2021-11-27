from PyQt5.QtGui import QFont, QPalette


class FontBuilder:
    def __init__(self):
        self.family = "Segoe UI"
        self.size = -1
        self.weight = -1
        self.style = None
        self.color = None

    def withFamily(self, family):
        self.family = family
        return self

    def withStyle(self, style):
        self.style = style
        return self

    def withSize(self, size):
        self.size = size
        return self

    def withWeight(self, weight):
        self.weight = weight
        return self

    # def withColor(self, color):
        # self.color = color
        # return self

    def build(self):
        font = QFont()
        font.setFamily(self.family)
        font.setPointSize(self.size)
        font.setItalic(self.style == "italic")
        font.setBold(self.weight == "bold")
        # if self.color is not None:
            # font.setPalette(self.color)
        self.size = -1
        self.weight = -1
        self.style = None
        self.color = None
        self.family = "Segoe UI"
        return font


# class Font:
