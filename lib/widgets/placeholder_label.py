from PyQt5.QtWidgets import QLineEdit


class LabelWithPlaceholder(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.placeholder = ""
        self.isDisplayingPlaceholder = False

    def setPlaceholderText(self, text: str):
        self.placeholderText = text
        self.__showPlaceholder()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.__cleanText()

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.__showPlaceholder()

    def __showPlaceholder(self):
        if self.text() == "":
            self.setText(self.placeholderText)
            self.isDisplayingPlaceholder = True

    def __cleanText(self):
        if self.isDisplayingPlaceholder:
            self.isDisplayingPlaceholder = False
            self.setText("")

    def text(self):
        if self.isDisplayingPlaceholder:
            return ""
        return super().text()
