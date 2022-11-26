from modules.screens.windows.MainWindowView import MainWindowView
from modules.statics.view import Material


class Application:
    def __init__(self):
        Material.Cursors.init_value()
        Material.Icons.init_value()

        self.window = MainWindowView().with_title_bar_height(24)
        self.window.apply_light_mode()

    def run(self) -> None:
        self.window.show()
