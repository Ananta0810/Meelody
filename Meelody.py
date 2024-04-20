from sys import argv, exit

from PyQt5.QtCore import Qt

from app.components.applications import SingletonApplication
from app.resource.qt import Icons, Cursors
from app.views.main_window import MainWindow


# def _initConsole():
#     if sys.stderr is None:
#         stream = io.StringIO()
#         sys.stdout = stream
#         sys.stderr = stream


# def _run_ffmpeg():
#     basedir = str(os.path.dirname(os.path.abspath(__file__)))
#     startupInfo = subprocess.STARTUPINFO()
#     startupInfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
#     subprocess.call(f'{basedir}/ffmpeg.exe', startupinfo=startupInfo)


def run_application():
    # _initConsole()
    # _run_ffmpeg()

    APP_NAME = "MeelodX"

    app = SingletonApplication(argv, APP_NAME)
    app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)
    app.setApplicationName(APP_NAME)

    Icons.init()
    Cursors.init()
    application = MainWindow()
    application.show()

    # Times.measure(lambda: application, lambda time: print(f"Time to start application: {time}"))

    exit(app.exec_())


if __name__ == '__main__':
    run_application()
