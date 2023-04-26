from sys import argv, exit
from PyQt5.QtWidgets import QApplication

from modules.helpers import Timers
from modules.screens.Application import Application


def run_application():
    app = QApplication(argv)
    application = Application()
    time_to_run = Timers.measure(lambda: application.run())
    print(f"Time to start application: {time_to_run}")
    exit(app.exec_())


if __name__ == '__main__':
    run_application()
