import io
import sys
from sys import argv, exit

from PyQt5.QtWidgets import QApplication

from modules.helpers import Times
from modules.screens.Application import Application
from modules.statics.view.Material import Icons

stream = io.StringIO()
sys.stdout = stream
sys.stderr = stream


def run_application():
    app = QApplication(argv)
    Times.measure(lambda: Application().run(), lambda time: print(f"Time to start application: {time}"))
    app.setWindowIcon(Icons.LOGO)
    exit(app.exec_())


if __name__ == '__main__':
    run_application()
