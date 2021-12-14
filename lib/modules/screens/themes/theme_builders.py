from modules.screens.qss.qss_elements import Background, Color, ColorBox

from .theme_builder import ThemeBuilder, ThemeData


class ButtonThemeBuilder(ThemeBuilder):
    lightModeTextColor: ColorBox = None
    darkModeTextColor: ColorBox = None
    lightModeBackground: Background = None
    darkModeBackground: Background = None
    lightModeCheckedBackground: Background = None
    darkModeCheckedBackground: Background = None

    def addLightModeTextColor(self, color: Color):
        self.lightModeTextColor = color
        return self

    def addDarkModeTextColor(self, color: Color):
        self.darkModeTextColor = color
        return self

    def addLightModeBackground(self, background: Background):
        self.lightModeBackground = background
        return self

    def addDarkModeBackground(self, background: Background):
        self.darkModeBackground = background
        return self

    def addLightModeActiveBackground(self, background: Background):
        self.lightModeCheckedBackground = background
        return self

    def addDarkModeActiveBackground(self, background: Background):
        self.darkModeCheckedBackground = background
        return self

    def build(self, itemSize: int) -> ThemeData:
        lightMode = (
            None
            if self.lightModeTextColor is None
            and self.lightModeBackground is None
            and self.lightModeCheckedBackground is None
            else self.__buildTheme(
                itemSize,
                self.lightModeTextColor,
                self.lightModeBackground,
                self.lightModeCheckedBackground,
            )
        )
        darkMode = (
            lightMode
            if self.darkModeTextColor is None
            and self.darkModeBackground is None
            and self.darkModeCheckedBackground is None
            else self.__buildTheme(
                itemSize,
                self.darkModeTextColor,
                self.darkModeBackground,
                self.darkModeCheckedBackground,
            )
        )
        return ThemeData(lightMode, darkMode)

    def __buildTheme(
        self,
        buttonSize,
        textColor: ColorBox,
        background: Background,
        checkedBackground: Background,
    ):
        styleSheet = ""
        if background is not None:
            styleSheet += BackgroundBuilder().export(
                "QPushButton", buttonSize, textColor, background
            )
        if checkedBackground is not None:
            styleSheet += BackgroundBuilder().export(
                "QPushButton:checked", buttonSize, textColor, checkedBackground
            )
        return styleSheet


class LabelThemeBuilder(ThemeBuilder):
    def __init__(self):
        self.lightModeTextColor = None
        self.darkModeTextColor = None
        self.lightModeBackground = None
        self.darkModeBackground = None

    def addLightModeTextColor(self, color: ColorBox):
        self.lightModeTextColor = color
        return self

    def addDarkModeTextColor(self, color: ColorBox):
        self.darkModeTextColor = color
        return self

    def addLightModeBackground(self, background: Background):
        self.lightModeBackground = background
        return self

    def addDarkModeBackground(self, background: Background):
        self.darkModeBackground = background
        return self

    def build(self, itemSize) -> ThemeData:
        lightMode = self.__buildTheme(
            itemSize, self.lightModeTextColor, self.lightModeBackground
        )
        darkMode = self.__buildTheme(
            itemSize,
            self.darkModeTextColor or self.lightModeTextColor,
            self.darkModeBackground or self.lightModeBackground,
        )
        return ThemeData(lightMode, darkMode)

    def __buildTheme(self, itemSize, textColor, background: Background) -> str:
        return BackgroundBuilder().export(
            "QLineEdit", itemSize, textColor, background
        )


class BackgroundBuilder:
    def export(
        self,
        element: str,
        elementSize: float,
        textColor: ColorBox,
        background: Background,
    ):
        normalContent = self.buildContent(textColor, background, elementSize)
        hoverContent = self.buildContent(
            textColor, background, elementSize, isHover=True
        )
        return (
            f"{element}"
            + "{"
            + f"{normalContent}"
            + "}"
            + f"{element}:hover"
            + "{"
            + f"{hoverContent}"
            + "}"
        )

    def buildContent(self, color, background, elementSize, isHover=False):
        content = ""
        if color is not None:
            content += f"color:{color.toStylesheet(isHover)};"
        content += (
            (
                f"border:{background.borderStyleSheet(isHover)};"
                + f"border-radius:{background.borderRadiusStyleSheet(elementSize)};"
                + f"background-color:{background.colorStyleSheet(isHover)};"
            )
            if background is not None
            else "border:none;background:transparent;"
        )
        return content


class HorizontalSliderThemeBuilder(ThemeBuilder):
    background: Background
    handleColor: ColorBox
    lineColor: ColorBox
    handleSize: int
    lineSize: int

    def __init__(self):
        self.lightModeBackground = None
        self.darkModeBackground = None
        self.lightHandleColor = None
        self.darkHandleColor = None
        self.lightLineColor = None
        self.darkLineColor = None
        self.handleSize = 10
        self.lineSize = 2

    def addLightModeBackground(self, background: Background):
        self.lightModeBackground = background
        return self

    def addDarkModeBackground(self, background: Background):
        self.darkModeBackground = background
        return self

    def addLightHandleColor(self, handleColor: ColorBox):
        self.lightHandleColor = handleColor
        return self

    def addDarkHandleColor(self, handleColor: ColorBox):
        self.darkHandleColor = handleColor
        return self

    def addLightLineColor(self, lineColor: ColorBox):
        self.lightLineColor = lineColor
        return self

    def addDarkLineColor(self, lineColor: ColorBox):
        self.darkLineColor = lineColor
        return self

    def addHandleSize(self, handleSize: int):
        self.handleSize = handleSize
        return self

    def addLineSize(self, lineSize: int):
        self.lineSize = lineSize
        return self

    def build(self, itemSize: int) -> ThemeData:
        lightMode = self.__getThemeContent(
            self.lightModeBackground,
            self.lightHandleColor,
            self.lightLineColor,
            itemSize,
        )
        darkMode = self.__getThemeContent(
            self.darkModeBackground or self.lightModeBackground,
            self.darkHandleColor or self.lightHandleColor,
            self.darkLineColor or self.lightLineColor,
            itemSize,
        )
        return ThemeData(lightMode, darkMode)

    def __getThemeContent(self, background, handleColor, lineColor, itemSize):
        lineRadius = self.lineSize // 2
        lineMargin = (itemSize - self.lineSize) // 2
        handleMargin = (itemSize - self.handleSize) // 2
        styleSheet = "QSlider::groove{border:none}"
        styleSheet += (
            (
                "QSlider{"
                + f"    background-color:{background.colorStyleSheet()};"
                + f"    border:{background.borderStyleSheet()};"
                + f"    border-radius:{background.borderRadiusStyleSheet(itemSize)}"
                + "}"
                + "QSlider::hover{"
                + f"    border:{background.borderStyleSheet(True)};"
                + f"    background:{background.colorStyleSheet(True)};"
                + "}"
            )
            if background is not None
            else "QSlider{border:None;background:transparent}"
        )
        styleSheet += (
            "QSlider::add-page{"
            + "     border:none;"
            + f"    background:{lineColor.toStylesheet()};"
            + f"    border-radius:{lineRadius}px;"
            + f"    margin:{lineMargin}px {handleMargin}px {lineMargin}px 0px"
            + "}"
            + "QSlider::sub-page{"
            + "     border:none;"
            + f"    background:{handleColor.toStylesheet()};"
            + f"    border-radius:{lineRadius}px;"
            + f"    margin:{lineMargin}px 0px {lineMargin}px {handleMargin + 1}px"
            + "}"
            + "QSlider::handle{"
            + "    border:none;"
            + f"    background:{handleColor.toStylesheet()};"
            + f"    border-radius:{self.handleSize // 2}px;"
            + f"    width:{self.handleSize}px;"
            + f"    margin:{handleMargin}px {handleMargin + 1}px"
            + "}"
            + "QSlider::handle:hover{"
            + f"    background:{handleColor.toStylesheet(True)};"
            + f"    width:{self.handleSize + 2}px;"
            + f"    border-radius:{self.handleSize // 2 + 1}px;"
            + f"    margin:{handleMargin - 1}px {handleMargin}px"
            + "}"
        )
        return styleSheet
