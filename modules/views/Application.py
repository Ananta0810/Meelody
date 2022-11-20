from modules.statics.view import Apps
from modules.views.windows.MainWindowView import MainWindowView


class Application:
    def __init__(self):
        Apps.Cursors.init_value()
        Apps.Icons.init_value()

        self.window = MainWindowView().with_title_bar_height(24)
        self.window.apply_dark_mode()

    def run(self) -> None:
        self.window.show()