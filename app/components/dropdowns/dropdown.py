from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QShowEvent
from PyQt5.QtWidgets import QComboBox, QWidget, QStyledItemDelegate

from app.common.statics.qt import Cursors
from app.components.base import Component
from app.helpers.stylesheets.translators.classname_translator import ClassNameTheme, ClassNameTranslator
from app.utils.base import Strings


class DropDown(QComboBox, Component):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        super()._initComponent()

    def _createUI(self) -> None:
        self.view().window().setWindowFlags(Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.view().window().setAttribute(Qt.WA_TranslucentBackground)
        self.setCursor(Cursors.pointer)
        self.view().setCursor(Cursors.pointer)
        self.setItemDelegate(QStyledItemDelegate())

    def setClassName(self, *classNames: str) -> None:
        light, dark = ClassNameTranslator.translateElements(Strings.join(" ", classNames), self)

        self._lightModeStyle = self.__buildStyle(light, True)
        self._darkModeStyle = self.__buildStyle(dark, False)

    @staticmethod
    def __buildStyle(theme: ClassNameTheme, lightMode: bool) -> str:
        normal = theme.getElement()
        return (
            f"""
            QComboBox {{ 
                {normal.state().toProps([
                "padding: 8px 16px",
                "color: black",
                "border-radius: 4px",
                "border: 1px solid rgb(230, 230, 230)",
                "background-color: rgb(255, 255, 255)"])} 
            }}
            QComboBox:hover, QPushButton:hover {{ 
                {normal.state("hover").toProps(["background-color: rgb(248, 248, 248)"])} 
            }}
            QComboBox::drop-down {{ border: none; background-color: transparent; min-width: 4px; }}
            QComboBox::down-arrow {{
                right: 8px;
                width: 8px;
                height: 8px;
                image: url('resource/images/icons/{"chevron-down.png" if lightMode else "chevron-down-light.png"}');
            }}
            QComboBox QAbstractItemView {{
                outline: 0px;
                margin-top: 4px;
                {theme.getElement("dropdown").state().toProps([
                "padding: 4px",
                "border-radius: 4px",
                "border: 1px solid rgb(230, 230, 230)",
                "background-color: rgb(255, 255, 255)"])}
            }}
            QComboBox QAbstractItemView::item {{ 
                {theme.getElement("item").state().toProps([
                "padding: 4px 8px",
                "border-radius: 4px",
                "border: none",
                "background-color: transparent",
                "color: black", ])}
            }}
            QComboBox QAbstractItemView::item:hover,QComboBox QAbstractItemView::item:focus {{ 
                {theme.getElement("item").state("hover").toProps(["background-color: rgb(240, 240, 240)"])} 
            }}
             """
        )

    def showEvent(self, e: Optional[QShowEvent]) -> None:
        super().showEvent(e)
        self.applyTheme()
