from abc import ABC, abstractmethod

from modules.screens.qss.qss_elements import (
    Background,
    Color,
    ColorBox,
    Padding,
)


class ThemeData:
    def __init__(self, lightMode, darkMode):
        self.lightMode = lightMode
        self.darkMode = darkMode or lightMode

    def __str__(self):
        return f"Light: {self.lightMode}, Dark: {self.darkMode}"


class ThemeBuilder(ABC):
    @abstractmethod
    def addLightModeBackground(self, background: Background):
        pass

    @abstractmethod
    def addDarkModeBackground(self, background: Background):
        pass

    @abstractmethod
    def build(self, itemSize: int) -> ThemeData:
        pass


class DropdownMenuThemeBuilder(ThemeBuilder):
    padding: Padding = None
    lightModeTextColor: ColorBox = None
    darkModeTextColor: ColorBox = None
    lightModeMenuTextColor: ColorBox = None
    darkModeMenuTextColor: ColorBox = None
    lightModeBackground: Background = None
    darkModeBackground: Background = None
    lightModeMenuBackground = None
    darkModeMenuBackground = None
    lightModeItemBackground = None
    darkModeItemBackground = None

    def addPadding(self, padding: Padding):
        self.padding = padding
        return self

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

    def addLightModeMenuTextColor(self, color: ColorBox):
        self.lightModeMenuTextColor = color
        return self

    def addDarkModeMenuTextColor(self, color: ColorBox):
        self.darkModeMenuTextColor = color
        return self

    def addLightModeMenuBackground(self, background: Background):
        self.lightModeMenuBackground = background
        return self

    def addDarkModeMenuBackground(self, background: Background):
        self.darkModeMenuBackground = background
        return self

    def addLightModeItemBackground(self, background: Background):
        self.lightModeItemBackground = background
        return self

    def addDarkModeItemBackground(self, background: Background):
        self.darkModeItemBackground = background
        return self

    def build(self, itemSize: int = 0) -> ThemeData:
        lightMode = self.__buildStyle(
            self.padding,
            self.lightModeTextColor,
            self.lightModeMenuTextColor,
            self.lightModeBackground,
            self.lightModeMenuBackground,
            self.lightModeItemBackground,
            itemSize,
        )

        darkMode = (
            lightMode
            if (
                self.darkModeTextColor is None
                and self.darkModeMenuTextColor is None
                and self.darkModeBackground is None
                and self.darkModeMenuBackground is None
                and self.darkModeItemBackground is None
            )
            else self.__buildStyle(
                self.padding,
                self.darkModeTextColor,
                self.darkModeMenuTextColor,
                self.darkModeBackground,
                self.darkModeMenuBackground,
                self.darkModeItemBackground,
                itemSize,
                dropDownArrowImage="assets/images/icons/chevron-down-light.png",
            )
        )
        return ThemeData(lightMode, darkMode)

    def __buildStyle(
        self,
        padding: Padding,
        color: ColorBox,
        menuTextColor: ColorBox,
        background: Background,
        menuBackground: Background,
        itemBackground: Background,
        elementSize: int,
        dropDownArrowSize: int = 8,
        dropDownArrowImage: str = "assets/images/icons/chevron-down.png",
    ):
        arrowBackgroundWidth = 20 + padding.getWidth()
        mainPadding = 0
        menuPadding = 0
        itemPadding = 0
        if padding is not None:
            mainPadding = padding.toStylesheet(elementSize)
            menuPadding = padding.toStylesheetWithRatio(elementSize, 0.333)
            itemPadding = padding.toStylesheetWithRatio(elementSize, 0.677)

        styleSheet = (
            "QComboBox {"
            + f"    padding:{mainPadding};"
            + f"    color:{'black' if color is None else color.toStylesheet()};"
            + f"    border:{background.borderStyleSheet()};"
            + f"    border-radius:{background.borderRadiusStyleSheet(elementSize)};"
            + f"    background-color:{background.colorStyleSheet()};"
            + "}"
            + "QComboBox:hover, QPushButton:hover{"
            + f"    border-color: {'#4032ff' if background.border is None or background.border.color is None else background.border.color.toStylesheet(True)}"
            + "}"
            + "QComboBox QAbstractItemView"
            + "{"
            + "    margin-top: 4px;"
            + f"    padding: {menuPadding};"
            + (
                f"    border: {menuBackground.borderStyleSheet()};"
                + f"    border-radius: {menuBackground.borderRadiusStyleSheet(elementSize)};"
                + f"    background-color: {menuBackground.colorStyleSheet()};"
                if menuBackground is not None
                else ""
            )
            + "}"
            + "QComboBox::drop-down {"
            + "    border:none;"
            + "    background-color:transparent;"
            + f"    min-width: {arrowBackgroundWidth}px;"
            + " }"
            + "QComboBox::down-arrow{"
            + f"    right: {menuPadding};"
            + f"    width: {dropDownArrowSize};"
            + f"    height: {dropDownArrowSize};"
            + f"    image: url('{dropDownArrowImage}');"
            + "}"
            + " /* Menu */"
            + "QComboBox QAbstractItemView::item{"
            + "    min-height: 32px;"
            + f"    padding: {itemPadding};"
            + (
                f"    border-radius: {itemBackground.borderRadiusStyleSheet(elementSize)};"
                + f"    border: {itemBackground.borderStyleSheet()};"
                + f"    background-color: {itemBackground.colorStyleSheet()};"
                if itemBackground is not None
                else ""
            )
            + f"    color:{'black' if menuTextColor is None else menuTextColor.toStylesheet()};"
            "}"
            + "QComboBox QAbstractItemView::item:hover,QComboBox QAbstractItemView::item:focus{"
            + (
                f"    border: {itemBackground.borderStyleSheet(True)};"
                + f"    border-radius: {itemBackground.borderRadiusStyleSheet(elementSize)};"
                + f"    background-color: {itemBackground.colorStyleSheet(True)};"
                if itemBackground is not None
                else ""
            )
            + f"    color:{'black' if menuTextColor is None else menuTextColor.toStylesheet(True)};"
            "}"
            + "QComboBox:editable {"
            + "    background-color:transparent;"
            + "    border:none;"
            + "}"
            + "QComboBox QAbstractItemView{outline:0px;}"
            + "QComboBox::indicator{"
            + "    background-color:transparent;"
            + "    selection-background-color:transparent;"
            + "    color:transparent;"
            + "    selection-color:transparent;"
            + "}"
        )
        return styleSheet


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
            "border:none;background-color:transparent"
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
        self.padding = 0

    def addPadding(self, padding: int):
        self.padding = padding
        return self

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

    def build(self, itemSize: int = 0) -> ThemeData:
        lightMode = self.__buildTheme(
            itemSize, self.lightModeTextColor, self.lightModeBackground
        )
        darkMode = self.__buildTheme(
            itemSize,
            self.darkModeTextColor or self.lightModeTextColor,
            self.darkModeBackground or self.lightModeBackground,
        )
        return ThemeData(lightMode, darkMode)

    def __buildTheme(
        self, itemSize: int, textColor: ColorBox, background: Background
    ) -> str:
        return BackgroundBuilder().export(
            "QLineEdit", itemSize, textColor, background, padding=self.padding
        )


class BackgroundBuilder:
    def export(
        self,
        element: str,
        elementSize: float,
        textColor: ColorBox,
        background: Background,
        padding: int = 0,
    ):
        normalContent = self.buildContent(
            padding, textColor, background, elementSize
        )
        hoverContent = self.buildContent(
            padding, textColor, background, elementSize, isHover=True
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

    def buildContent(
        self, padding, color, background, elementSize, isHover=False
    ):
        content = ""
        if color is not None:
            content += f"color:{color.toStylesheet(isHover)};"
        content += (
            (
                f"padding:{padding}px;"
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
