import traceback
from sys import argv, exit

from PyQt5.QtCore import Qt

from app.components.applications import SingletonApplication
from app.views import Application


# """
#     - pip install PyQt5
#     - pip install pygame==2.5.2
#     - pip install eyed3==0.9.7
#     - pip install Pillow==9.5.0
#     - pip install pillow==9.5.0
#     - pip install pydub==0.25.0
#     - pip install pytube==15.0.0
# """


def runApplication():
    APP_NAME = "Meelody"

    app = SingletonApplication(argv, APP_NAME)
    app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)
    app.setApplicationName(APP_NAME)

    Application().run()

    exit(app.exec_())


if __name__ == '__main__':
    try:
        runApplication()
    except Exception as e:
        traceback.print_exc()
