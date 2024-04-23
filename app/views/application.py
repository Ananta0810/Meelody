from app.resource.qt import Icons, Cursors
from app.views.windows import MainWindow


class Application:
    def __init__(self):
        self.__createUI()
        self.__configureDatabase()

    def __createUI(self):
        Icons.init()
        Cursors.init()
        self.window = MainWindow()

    def __configureDatabase(self):
        self.window.applyLightMode()

    def run(self) -> None:
        self.window.show()

    def receiveMessage(self, msg: str) -> None:
        self.window.receiveMessage(msg)
