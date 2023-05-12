import io
import sys
from sys import argv, exit

from PyQt5.QtCore import Qt

from modules.helpers import Times
from modules.screens.Application import Application
from modules.statics.view.Material import Icons
from modules.widgets.Applications import SingletonApplication

if sys.stderr is None:
    stream = io.StringIO()
    sys.stdout = stream
    sys.stderr = stream


def run_application():
    APP_NAME = "Meelody"
    app = SingletonApplication(argv, APP_NAME)
    app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)
    app.setApplicationName(APP_NAME)
    application = Application()
    app.messageSent.connect(application.receiveMessage)
    Times.measure(lambda: application.run(), lambda time: print(f"Time to start application: {time}"))
    app.setWindowIcon(Icons.LOGO)
    exit(app.exec_())


if __name__ == '__main__':
    run_application()
