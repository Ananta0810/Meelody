from typing import final

from PyQt5.QtGui import QFont


@final
class FontFactory:
    @staticmethod
    def create(family: str = "Segoe UI", size: int = 9, italic: bool = False, bold: bool = False) -> QFont:
        font = QFont(family)
        font.setPointSize(size)
        font.setItalic(italic)
        font.setBold(bold)
        return font
