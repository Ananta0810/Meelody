from modules.views.windows.MainWindow import MainWindow


class Application:
    def __init__(self):
        self.window = MainWindow().with_title_bar_height(24)

    def run(self) -> None:
        self.window.show()