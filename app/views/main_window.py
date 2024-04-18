from app.components.windows import FramelessWindow


class MainWindow(FramelessWindow):

    def __init__(self, width: int = 1280, height: int = 720):
        super().__init__()
        self.setFixedWidth(width)
        self.setFixedHeight(height)

        self.installEventFilter(self)
