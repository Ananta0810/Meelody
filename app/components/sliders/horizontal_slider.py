from abc import ABC

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSlider, QWidget

from app.components.base import Component
from app.helpers.base import Strings
from app.helpers.stylesheets import Backgrounds
from app.helpers.stylesheets.translators import ClassNameTranslator
from app.helpers.stylesheets.translators.classname_translator import ClassNameTheme


class HorizontalSlider(QSlider, Component, ABC):

    def __init__(self, parent: QWidget | None = None):
        QSlider.__init__(self, parent)
        self.__currentClassName = ""
        self._handleHeight = 10
        self._trackSize = 2
        self.setOrientation(Qt.Horizontal)

    def setSliderSize(self, handle: int, track: int = 2) -> None:
        self._handleHeight = handle
        self._trackSize = track
        self.setClassName(self.__currentClassName)

    def setClassName(self, *classNames: str) -> None:
        self.__currentClassName = Strings.join(classNames, " ")

        light, dark = ClassNameTranslator.translateElements(self.__currentClassName, self)

        self._lightModeStyle = self.__buildStyle(light)
        self._darkModeStyle = self.__buildStyle(dark)

    def __buildStyle(self, theme: ClassNameTheme) -> str:
        trackRadius = self._trackSize // 2

        itemSize = self.maximumHeight()
        trackMargin = (itemSize - self._trackSize) // 2
        handleMargin = (itemSize - self._handleHeight) // 2

        sliderBg = theme.getElement("none").state("none").toProps() or Backgrounds.NONE.toStylesheet()
        trackLeft = theme.getElement("track").state("active").toProps() or Backgrounds.PRIMARY.toStylesheet()
        trackRight = theme.getElement("track").state("none").toProps() or Backgrounds.GRAY.withOpacity(50).toStylesheet()
        handle = theme.getElement("handle").state("none").toProps() or Backgrounds.PRIMARY.toStylesheet()
        handleActive = theme.getElement("handle").state("active").toProps() or handle

        return f"""
             QSlider {{{sliderBg}}}
             QSlider::groove{{border:none}}
             QSlider::sub-page {{
                 border:none;
                 border-radius:{trackRadius}px;
                 margin:{trackMargin}px 0px {trackMargin}px {handleMargin + 1}px;
                 {trackLeft}
             }}
             QSlider::add-page {{
                 border:none;
                 border-radius:{trackRadius}px;
                 margin:{trackMargin}px {handleMargin}px {trackMargin}px 0px;
                 {trackRight}
             }}
             QSlider::handle {{
                 border:none;
                 border-radius:{self._handleHeight // 2}px;
                 width:{self._handleHeight}px;
                 margin:{handleMargin}px {handleMargin + 1}px;
                 {handle}
             }}
             QSlider::handle:hover {{
                 width:{self._handleHeight + 2}px;
                 border-radius:{self._handleHeight // 2 + 1}px;
                 margin:{handleMargin - 1}px {handleMargin}px;
                 {handleActive}
             }}
             """
