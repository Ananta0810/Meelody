import io
import os
import subprocess
import sys
from sys import argv, exit

from PyQt5.QtCore import Qt

from modules.helpers import Times
from modules.screens.Application import Application
from modules.statics.view.Material import Icons
from modules.widgets.Applications import SingletonApplication


def _initConsole():
    if sys.stderr is None:
        stream = io.StringIO()
        sys.stdout = stream
        sys.stderr = stream


def _run_ffmpeg():
    basedir = str(os.path.dirname(os.path.abspath(__file__)))
    startupInfo = subprocess.STARTUPINFO()
    startupInfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    subprocess.call(f'{basedir}/ffmpeg.exe', startupinfo=startupInfo)


def run_application():
    _initConsole()
    _run_ffmpeg()

    APP_NAME = "Meelody"

    app = SingletonApplication(argv, APP_NAME)
    app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)
    app.setApplicationName(APP_NAME)
    application = Application()
    app.messageSent.connect(application.receiveMessage)
    app.setWindowIcon(Icons.LOGO)

    Times.measure(lambda: application.run(), lambda time: print(f"Time to start application: {time}"))

    exit(app.exec_())


if __name__ == '__main__':
    run_application()
