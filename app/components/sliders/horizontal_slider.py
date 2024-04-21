from abc import ABC

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSlider, QWidget

from app.components.base import Component
from app.helpers.base import Strings, Dicts
from app.helpers.stylesheets import Background
from app.helpers.stylesheets.translators import ClassNameTranslator


class HorizontalSlider(QSlider, Component, ABC):

    def __init__(self, parent: QWidget | None = None):
        QSlider.__init__(self, parent)
        self.setOrientation(Qt.Horizontal)

    def setClassName(self, *classNames: str) -> None:
        light, dark = ClassNameTranslator.translateToVariants(Strings.join(classNames, " "), self)

        style = self.__buildStyle(light)
        self._lightModeStyle = style
        self._darkModeStyle = self.__buildStyle(dark)

    def __buildStyle(self, theme):
        handleSize: int = 10
        lineSize: int = 2
        itemSize = self.maximumHeight()
        lineRadius = lineSize // 2
        lineMargin = (itemSize - lineSize) // 2
        handleMargin = (itemSize - handleSize) // 2
        element, normalStyle = Dicts.getFrom(theme, "",
                                             otherwise=(
                                             ClassNameTranslator.typeNameOf(self), [Background().toStylesheet()]))
        return f"""
             {element} {{{Strings.join(normalStyle, ";")}}}
             QSlider::groove{{border:none}}
             QSlider::add-page {{
                 border:none;
                 border-radius:{lineRadius}px;
                 margin:{lineMargin}px {handleMargin}px {lineMargin}px 0px;
                 {Strings.join(theme["track"][''][1], ";")}
             }}
             QSlider::sub-page {{
                 border:none;
                 border-radius:{lineRadius}px;
                 margin:{lineMargin}px 0px {lineMargin}px {handleMargin + 1}px;
                 {Strings.join(theme["track"][''][1], ";")}
             }}
             QSlider::handle {{
                 border:none;
                 border-radius:{handleSize // 2}px;
                 width:{handleSize}px;
                 margin:{handleMargin}px {handleMargin + 1}px;
                 {Strings.join(theme["handler"][''][1], ";")}
             }}
             QSlider::handle:hover {{
                 width:{handleSize + 2}px;
                 border-radius:{handleSize // 2 + 1}px;
                 margin:{handleMargin - 1}px {handleMargin}px;
                 {Strings.join(theme["handler"][''][1], ";")}
             }}
             """
