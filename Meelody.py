from sys import argv, exit

from PyQt5.QtCore import Qt

from app.components.applications import SingletonApplication
from app.helpers.others import Times
from app.views import Application


# """
#     - pip install PyQt5
#     - pip install pygame==2.5.2
#     - pip install eyed3==0.9.7
#     - pip install yt-dlp==2023.2.17
#     - pip install Pillow==9.5.0
#     - pip install pillow==9.5.0
#     - pip install pydub==0.25.0
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
