from typing import Optional, Self, Union

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QWidget

from modules.helpers.types.Decorators import override
from modules.models.view.builder.BackgroundThemeBuilder import BackgroundThemeBuilder
from modules.models.view.builder.TextStyle import TextStyle
from modules.views.ViewComponent import ViewComponent


class LabelWithDefaultText(QLabel, ViewComponent):
    def __init__(self, parent: Optional["QWidget"] = None):
        super().__init__(parent)
        self.default_text: str = ""
        self.light_mode_style: str = ''
        self.dark_mode_style: str = ''

    @override
    def setText(self, text: str) -> None:
        return super().setText(text or self.default_text)

    def set_default_text(self, text: str) -> None:
        if self.text() == self.default_text:
            self.setText(text)
        self.default_text = text

    @override
    def apply_light_mode(self):
        self.setStyleSheet(self.light_mode_style)

    @override
    def apply_dark_mode(self):
        self.setStyleSheet(self.dark_mode_style)

    @staticmethod
    def build(
        font: QFont,
        light_mode_style: TextStyle,
        dark_mode_style: TextStyle = None,
        width: Union[int, None] = None,
        padding: int = 0,
        allow_multiple_lines: bool = True,
        parent: Optional["QWidget"] = None,
    ) -> Self:
        label = LabelWithDefaultText(parent)
        label.setFont(font)
        label.setWordWrap(allow_multiple_lines)
        if width is not None:
            label.setFixedWidth(width)
        label.light_mode_style = LabelWithDefaultText.build_style(light_mode_style, padding, width)
        label.dark_mode_style = LabelWithDefaultText.build_style(dark_mode_style or light_mode_style, padding, width)
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
