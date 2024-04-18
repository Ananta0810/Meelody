import sys
from typing import List

from PyQt5.QtCore import pyqtSignal, QSharedMemory, QIODevice
from PyQt5.QtNetwork import QLocalServer, QLocalSocket
from PyQt5.QtWidgets import QApplication


class SingletonApplication(QApplication):
    messageSent = pyqtSignal(object)

    def __init__(self, argv: List[str], key: str):
        super().__init__(argv)
        self.key = key
        self.timeout = 1000
        self.server = QLocalServer(self)
        self.memory = QSharedMemory(self)
        self.memory.setKey(key)

        if self.memory.attach():
            self.isRunning = True
            self.sendMessage(argv[1] if len(argv) > 1 else 'show')
            sys.exit(1)

        self.isRunning = False
        if not self.memory.create(1):
            raise RuntimeError(self.memory.errorString())

        self.server.newConnection.connect(self.__onNewConnection)
        self.server.listen(key)

    def __onNewConnection(self):
        socket = self.server.nextPendingConnection()
        if socket.waitForReadyRead(self.timeout):
            self.messageSent.emit(socket.readAll().data().decode('utf-8'))
            socket.disconnectFromServer()

    def sendMessage(self, message: str):
        """ send message to another application """
        if not self.isRunning:
            return

        # connect to another application
        socket = QLocalSocket(self)
        socket.connectToServer(self.key, QIODevice.WriteOnly)
        if not socket.waitForConnected(self.timeout):
            return

        # send message
        socket.write(message.encode("utf-8"))
        if not socket.waitForBytesWritten(self.timeout):
            return

        socket.disconnectFromServer()
