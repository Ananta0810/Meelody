from typing import Optional

from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QLabel, QWidget

from modules.helpers.types import Numbers
from modules.helpers.types.Decorators import override
from modules.models.view.Background import Background
from modules.screens.AbstractScreen import BaseView


class ProgressBar(QWidget, BaseView):
    __value: float = 0

    __bg_dark_mode_style: str = None
    __bg_light_mode_style: str = None
    __progress_dark_mode_style: str = None
    __progress_light_mode_style: str = None

    def __init__(self, parent: Optional["QWidget"] = None):
        super().__init__(parent)
        self.__init_ui()

    def __init_ui(self) -> None:
        self.__bar = QLabel(self)

    def set_value(self, value: float) -> None:
        self.__value = Numbers.clamp(float(value), float(0), float(100))
        self.__resize_bar()

    @override
    def resizeEvent(self, a0: QResizeEvent) -> None:
        super().resizeEvent(a0)
        self.__bar.setFixedHeight(self.height())
        self.__bar.setMaximumWidth(self.width())
        self.__resize_bar()

    def __resize_bar(self):
        self.__bar.setMinimumWidth(int(self.__value * self.width() / 100))

    def set_progress_style(self, light_mode: Background, dark_mode: Background = None) -> None:
        light_style = light_mode.to_stylesheet(border_radius_size=self.height() // 2)
        self.__progress_light_mode_style = light_style
        self.__progress_dark_mode_style = light_style \
            if dark_mode is None \
            else dark_mode.to_stylesheet(border_radius_size=self.height() // 2)

    def set_background_style(self, light_mode: Background, dark_mode: Background) -> None:
        light_style = light_mode.to_stylesheet(border_radius_size=self.height() // 2)
        self.__bg_light_mode_style = light_style
        self.__bg_dark_mode_style = light_style \
            if dark_mode is None \
            else dark_mode.to_stylesheet(border_radius_size=self.height() // 2)

    def apply_light_mode(self) -> None:
        self.__bar.setStyleSheet(self.__progress_light_mode_style or "")
        self.setStyleSheet(self.__bg_light_mode_style or "")

    def apply_dark_mode(self) -> None:
        self.__bar.setStyleSheet(self.__progress_dark_mode_style or "")
        self.setStyleSheet(self.__bg_dark_mode_style or "")
