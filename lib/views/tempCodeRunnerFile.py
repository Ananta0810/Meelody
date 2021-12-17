
if __name__ == "__main__":
    app = QApplication(argv)
    MainWindow = FramelessWindow()
    ui = ApplicationInterface()
    ui.setupUi(MainWindow)
    ui.lightMode()
    MainWindow.show()
    exit(app.exec_())
