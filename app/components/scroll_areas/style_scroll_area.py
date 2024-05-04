from typing import Optional

from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QScrollArea, QWidget

from app.components.base import Component
from app.helpers.base import Strings
from app.helpers.stylesheets.translators import ClassNameTranslator
from app.helpers.stylesheets.translators.classname_translator import ClassNameTheme


class StyleScrollArea(QScrollArea, Component):

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent=parent)
        self._scrollBarWidth = 4

        super().setContentsMargins(0, 0, 0, 0)
        super().setWidgetResizable(True)

    def resizeEvent(self, a0: QResizeEvent) -> None:
        super().resizeEvent(a0)
        self.widget().setFixedWidth(self.rect().width() - 4)

    def setClassName(self, *classNames: str) -> None:
        light, dark = ClassNameTranslator.translateElements(Strings.join(" ", classNames), self)

        self._lightModeStyle = self.__buildStyle(light)
        self._darkModeStyle = self.__buildStyle(dark)

    def __buildStyle(self, theme: ClassNameTheme) -> str:
        return f"""
            QScrollArea {{ background: transparent; border: none; }}
            QScrollArea > QWidget > QWidget {{ background: transparent; border: none; }}
            QScrollBar {{ background: palette(base); border: none; }}
            QScrollBar:vertical {{border:none;background-color:transparent;width:{self._scrollBarWidth}px}}
            QScrollBar::handle:vertical {{{theme.getElement("scroll").state("none").toProps() or ""}}}
            QScrollBar::handle:vertical:hover {{{theme.getElement("scroll").state("hover").toProps() or ""}}}
            QScrollBar::sub-line:vertical {{border:none}}
            QScrollBar::add-line:vertical {{border:none}}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{background-color:none}}
            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {{background-color:none}}
        """
