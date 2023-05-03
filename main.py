from sys import argv, exit
from PyQt5.QtWidgets import QApplication

from modules.helpers import Times
from modules.screens.Application import Application


def run_application():
    app = QApplication(argv)
    Times.measure(lambda: Application().run(), lambda time: print(f"Time to start application: {time}"))
    exit(app.exec_())


if __name__ == '__main__':
    run_application()
