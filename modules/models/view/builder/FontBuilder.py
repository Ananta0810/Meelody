from PyQt5.QtGui import QFont


class FontBuilder:

    @staticmethod
    def build(
        family: str = "Segoe UI",
        size: int = 9,
        italic: bool = False,
        bold: bool = False
    ) -> QFont:
        font = QFont(family)
        font.setPointSize(size)
        font.setItalic(italic)
        font.setBold(bold)
        return font
