from sys import argv, exit
from time import perf_counter
from PyQt5.QtWidgets import QApplication

from modules.screens.Application import Application

def run_application():
    print("starting...")
    start = perf_counter()
    app = QApplication(argv)
    application = Application()
    application.run()
    end = perf_counter()
    print(f"Time to start application: {end - start}")
    exit(app.exec_())

if __name__ == '__main__':
    run_application()

