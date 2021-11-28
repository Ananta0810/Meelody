from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsDropShadowEffect


class Effect:
    shadow = QGraphicsDropShadowEffect(
        blurRadius=50, color=QColor(128, 64, 255, 100), xOffset=0, yOffset=3
    )
