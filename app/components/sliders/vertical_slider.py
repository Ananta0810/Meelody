from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSlider, QWidget

from app.components.base import Component
from app.helpers.stylesheets import ClassNameTheme
from app.helpers.stylesheets import ClassNameTranslator
from app.utils.base import Strings
from app.utils.reflections import suppressException


class VerticalSlider(QSlider, Component):

    def __init__(self, parent: Optional[QWidget] = None):
        QSlider.__init__(self, parent)
        super()._initComponent()

        self._currentClassName = ""
        self._handleHeight = 10
        self._trackSize = 2
        self.setOrientation(Qt.Vertical)
        self.setInvertedAppearance(True)
        self.setInvertedControls(True)

    def setSliderSize(self, handle: int, track: int = 2) -> None:
        self._handleHeight = handle
        self._trackSize = track
        self.setClassName(self._currentClassName)

    @suppressException
    def setClassName(self, *classNames: str) -> None:
        self._currentClassName = Strings.join(" ", classNames)

        light, dark = ClassNameTranslator.translateElements(self._currentClassName, self)

        self._lightModeStyle = self.__buildStyle(light)
        self._darkModeStyle = self.__buildStyle(dark)

    def __buildStyle(self, theme: ClassNameTheme) -> str:
        trackRadius = self._trackSize // 2

        itemSize = self.maximumWidth()
        trackMargin = (itemSize - self._trackSize) // 2
        handleMargin = (itemSize - self._handleHeight) // 2

        sliderBg = theme.getElement("none").state("none").toProps(["background-color: transparent"])
        trackActive = theme.getElement("track").state("active").toProps(["background-color: rgb(100, 32, 255)"])
        trackInactive = theme.getElement("track").state("none").toProps(["background-color: rgba(128, 128, 128, 128)"])
        handle = theme.getElement("handle").state("none").toProps(["background-color: rgb(100, 32, 255)"])
        handleActive = theme.getElement("handle").state("active").toProps() or handle

        return f"""
             QSlider {{{sliderBg}}}
             QSlider::groove{{border:none}}
             QSlider::sub-page {{
                 border:none;
                 border-radius:{trackRadius}px;
                 margin: {handleMargin + 1}px {trackMargin}px 0px {trackMargin}px;
                 {trackActive}
             }}
             QSlider::add-page {{
                 border:none;
                 border-radius:{trackRadius}px;
                 margin: 0px {trackMargin}px {handleMargin}px {trackMargin}px;
                 {trackInactive}
             }}
             QSlider::handle {{
                 border:none;
                 border-radius:{self._handleHeight // 2}px;
                 height:{self._handleHeight}px;
                 margin:{handleMargin + 1}px {handleMargin}px;
                 {handle}
             }}
             QSlider::handle:hover {{
                 border-radius:{self._handleHeight // 2 + 1}px;
                 height:{self._handleHeight + 2}px;
                 margin:{handleMargin}px {handleMargin - 1}px;
                 {handleActive}
             }}
             """
