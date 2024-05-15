import typing
from typing import Optional, Union

from PyQt5.QtCore import pyqtBoundSignal, pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QPushButton

from app.components.buttons import ActionButton
from app.components.widgets import ExtendableStyleWidget, FlexBox


class DotPage(ExtendableStyleWidget):
    pageChanged: pyqtBoundSignal = pyqtSignal(int)

    def __init__(self, parent: Optional[QWidget] = None):
        self.__activeIndex = 0
        self.__total = 0

        super().__init__(parent)
        super()._initComponent()

    def _createUI(self) -> None:
        super()._createUI()

        self._layout = FlexBox(self)
        self._layout.setSpacing(8)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setAlignment(Qt.AlignHCenter)

    def setTotalPages(self, total: int) -> None:
        self._layout.clear()
        for pageNumber in range(0, total):
            self.__createPage(pageNumber)

        self.__total = total
        self.setActivePage(0)

    def __createPage(self, number: int) -> None:
        page = ActionButton()
        page.setFixedSize(8, 8)
        page.setClassName("rounded-full bg-primary-20 checked:bg-primary dark:bg-white-20 dark:checked:bg-white")
        page.setCheckable(True)
        self._layout.addWidget(page)

        page.clicked.connect(lambda: self.setActivePage(number))
        page.applyTheme()

    def setActivePage(self, pageNumber: int) -> None:
        for i in range(0, self.__total):
            page: QPushButton = self._layout.itemAt(i).widget()
            page.setChecked(i == pageNumber)

        if self.__activeIndex != pageNumber:
            self.pageChanged.emit(pageNumber)

        self.__activeIndex = pageNumber

    def nextPage(self) -> None:
        self.setActivePage((self.__activeIndex + 1) % self.__total)

    def previousPage(self) -> None:
        self.setActivePage((self.__activeIndex - 1 + self.__total) % self.__total)

    def setContentsMargins(self, left: int, top: int, right: int, bottom: int) -> None:
        self._layout.setContentsMargins(left, top, right, bottom)

    def setAlignment(self, alignment: Union[Qt.Alignment, Qt.AlignmentFlag]) -> None:
        self._layout.setAlignment(alignment)

    def setToolTip(self, a0: typing.Optional[str]) -> None:
        for i in range(0, self.__total):
            self._layout.itemAt(i).widget().setToolTip(a0)
