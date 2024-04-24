from sys import argv, exit

from PyQt5.QtCore import Qt

from app.components.applications import SingletonApplication
from app.helpers.others import Times
from app.views import Application


# """
#     - pip install PyQt5
#     - pip install pygame
#     - pip install eyed3
#     - pip install yt-dlp==2023.2.17
#     - pip install Pillow==9.0.0
#     - pip install pillow
# """


def runApplication():
    APP_NAME = "MeelodX"

    app = SingletonApplication(argv, APP_NAME)
    app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)
    app.setApplicationName(APP_NAME)

    Times.measure(lambda: Application().run(), lambda time: print(f"Time to start application: {time}"))

    exit(app.exec_())


if __name__ == '__main__':
    runApplication()
