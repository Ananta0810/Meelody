from PyQt5.QtGui import QFont, QFontDatabase


class FontBuilder:
    def __init__(self):
        self.family = "Segoe UI"
        self.size = 9
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

    def build(self):
        font = QFont(self.family)
        font.setPointSize(self.size)
        font.setItalic(self.style == "italic")
        font.setBold(self.weight == "bold")
        self.__init__()
        return font
