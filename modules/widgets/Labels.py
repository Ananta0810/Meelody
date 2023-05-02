from typing import Optional, Union, Callable

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QFontMetrics
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
    __is_fixed_with: bool = False

    def __init__(self, parent: Optional["QWidget"] = None):
        super().__init__(parent)

    @override
    def setFixedWidth(self, w: int) -> None:
        super().setFixedWidth(w)
        self.__is_fixed_with = True
        self.setText(self.__displaying_text)

    @override
    def setText(self, text: str) -> None:
        self.__displaying_text = text or self.__default_text
        if self.__is_fixed_with:
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


class DoubleClickedEditableLabel(QLineEdit, BaseView):
    __default_text: str = ""
    __light_mode_style: str
    __dark_mode_style: str
    __onchange_text: Callable[[str], None]

    def __init__(self, parent: Optional["QWidget"] = None):
        super().__init__(parent)

    def mouseDoubleClickEvent(self, event):
        super().mouseDoubleClickEvent(event)
        super().setReadOnly(False)

    def keyPressEvent(self, a0):
        super().keyPressEvent(a0)
        if a0.key() != Qt.Key_Return:
            return
        self.setReadOnly(True)
        try:
            self.__onchange_text(self.text())
        except AttributeError:
            print("Please assign onchange_text for DoubleClickedEditableLabel.")
            pass

    @handler
    def set_onchange_text(self, fn: Callable[[str], None]) -> None:
        self.__onchange_text = fn

    @override
    def setText(self, text: str) -> None:
        super().setText(text or self.__default_text)
        metrics = self.fontMetrics()
        self.setMinimumWidth(metrics.boundingRect(text).width() + 4)

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
        parent: Optional["QWidget"] = None,
    ) -> 'DoubleClickedEditableLabel':
        label = DoubleClickedEditableLabel(parent)
        label.setFont(font)
        label.setReadOnly(True)
        label.set_light_mode_style(LabelWithDefaultText.build_style(light_mode_style, padding, width))
        label.set_dark_mode_style(
            LabelWithDefaultText.build_style(dark_mode_style or light_mode_style, padding, width))
        return label


class Input(QLineEdit, BaseView):
    __default_text: str = ""
    __light_mode_style: str
    __dark_mode_style: str
    __onpresses: Callable[[str], None]

    def __init__(self, parent: Optional["QWidget"] = None):
        super().__init__(parent)

    @handler
    def set_onpressed(self, fn: Callable[[], None]) -> None:
        self.__onpresses = fn

    @override
    def keyPressEvent(self, a0):
        super().keyPressEvent(a0)
        if a0.key() != Qt.Key_Return:
            return
        if self.__onpresses is not None:
            self.__onpresses()

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
