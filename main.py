from sys import argv, exit
from PyQt5.QtWidgets import QApplication

from modules.helpers import Timers
from modules.screens.Application import Application


def run_application():
    app = QApplication(argv)
    application = Application()
    Timers.measure(lambda: application.run(), message="Time to start application: {}")
    exit(app.exec_())


if __name__ == '__main__':
    run_application()
