from PyQt5.QtGui import QFont


class FontBuilder:
    def __init__(self):
        self.family = "Segoe UI"
        self.size = 9
        self.weight = "normal"
        self.style = None

    def withFamily(self, family) -> None:
        self.family = family
        return self

    def withStyle(self, style: str) -> None:
        self.style = style
        return self

    def withSize(self, size: int) -> None:
        self.size = size
        return self

    def withWeight(self, weight: str) -> None:
        self.weight = weight
        return self

    def build(self) -> QFont:
        font = QFont(self.family)
        font.setPointSize(self.size)
        font.setItalic(self.style == "italic")
        font.setBold(self.weight == "bold")
        return font
