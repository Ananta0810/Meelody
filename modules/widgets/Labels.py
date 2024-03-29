from typing import Optional, Union, Callable

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QFontMetrics, QResizeEvent
from PyQt5.QtWidgets import QLabel, QWidget, QLineEdit

from modules.helpers.types.Decorators import override, handler
from modules.models.view.builder.BackgroundThemeBuilder import BackgroundThemeBuilder
from modules.models.view.builder.TextStyle import TextStyle
from modules.screens.AbstractScreen import BaseView


class LabelWithDefaultText(QLabel, BaseView):
    __default_text: str = ""
    __displaying_text: str = ""
    __light_mode_style: str
    __dark_mode_style: str
    __show_dot: bool = True

    def __init__(self, parent: Optional["QWidget"] = None):
        super().__init__(parent)

    def enable_ellipsis(self, a0: bool) -> None:
        self.__show_dot = a0

    @override
    def resizeEvent(self, a0: QResizeEvent) -> None:
        super().resizeEvent(a0)
        self.setText(self.__displaying_text)

    @override
    def setText(self, text: str) -> None:
        self.__displaying_text = text or self.__default_text
        if self.__show_dot:
            metrics = QFontMetrics(self.font())
            display_text_with_dot = metrics.elidedText(text, Qt.ElideRight, self.width())
            super().setText(display_text_with_dot)
            return
        return super().setText(self.__displaying_text)

    def text(self) -> str:
        return self.__displaying_text

    def set_default_text(self, text: str) -> None:
        self.__default_text = text

    def set_light_mode_style(self, style: str) -> None:
        self.__light_mode_style = style

    def set_dark_mode_style(self, style: str) -> None:
        self.__dark_mode_style = style

    @override
    def apply_light_mode(self):
        self.setStyleSheet(self.__light_mode_style)

    @override
    def apply_dark_mode(self):
        self.setStyleSheet(self.__dark_mode_style)

    @staticmethod
    def build(
        font: QFont,
        light_mode_style: TextStyle,
        dark_mode_style: TextStyle = None,
        width: Union[int, None] = None,
        padding: int = 0,
        allow_multiple_lines: bool = False,
        parent: Optional["QWidget"] = None,
    ) -> 'LabelWithDefaultText':
        label = LabelWithDefaultText(parent)
        label.setFont(font)
        label.setWordWrap(allow_multiple_lines)
        label.enable_ellipsis(not allow_multiple_lines)
        if width is not None:
            label.setFixedWidth(width)
        label.set_light_mode_style(LabelWithDefaultText.build_style(light_mode_style, padding, width))
        label.set_dark_mode_style(LabelWithDefaultText.build_style(dark_mode_style or light_mode_style, padding, width))
        return label

    @staticmethod
    def build_style(style: TextStyle, padding: int, size: int = 32):
        return BackgroundThemeBuilder.build(
            element=BackgroundThemeBuilder.LABEL,
            element_size=size,
            background=style.background,
            text_color=style.text_color,
            padding=padding
        )


class Input(QLineEdit, BaseView):
    __default_text: str = ""
    __light_mode_style: str
    __dark_mode_style: str
    __onpresses: Callable[[str], None] = None

    def __init__(self, parent: Optional["QWidget"] = None):
        super().__init__(parent)

    @handler
    def set_onpressed(self, fn: Callable[[str], None]) -> None:
        self.__onpresses = fn

    @override
    def keyPressEvent(self, a0):
        super().keyPressEvent(a0)
        if a0.key() != Qt.Key_Return:
            return
        if self.__onpresses is not None:
            self.__onpresses(self.text())

    @override
    def setText(self, text: str) -> None:
        super().setText(text or self.__default_text)
        metrics = self.fontMetrics()
        self.setMinimumWidth(metrics.boundingRect(text).width() + 4)

    def __set_light_mode_style(self, style: str) -> None:
        self.__light_mode_style = style

    def __set_dark_mode_style(self, style: str) -> None:
        self.__dark_mode_style = style

    @override
    def apply_light_mode(self):
        self.setStyleSheet(self.__light_mode_style)

    @override
    def apply_dark_mode(self):
        self.setStyleSheet(self.__dark_mode_style)

    @staticmethod
    def build(
        font: QFont,
        light_mode_style: TextStyle,
        dark_mode_style: TextStyle = None,
        width: Union[int, None] = None,
        padding: int = 0,
        parent: Optional["QWidget"] = None,
    ) -> 'Input':
        widget = Input(parent)
        widget.setFont(font)
        style = LabelWithDefaultText.build_style(light_mode_style, padding, width)
        widget.__set_light_mode_style(style)
        widget.__set_dark_mode_style(
            style if dark_mode_style is None else LabelWithDefaultText.build_style(dark_mode_style, padding, width)
        )
        return widget
