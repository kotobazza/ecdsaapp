import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

from PyQt6.QtCore import QObject, pyqtSignal, QDataStream, QByteArray, pyqtSlot
from PyQt6.QtNetwork import QTcpServer, QTcpSocket, QAbstractSocket, QHostAddress


class Server(QObject):
    messageReceived = pyqtSignal(str)
    tcpmodelError = pyqtSignal()

    def __init__(self, ports, parent=None):
        super().__init__()
        self.port = ports
        self.parent = parent
        self.clients = []
        
        self.__init_server()
    
    def __init_server(self):
        
        self.server = QTcpServer(self)
        self.client_connection = None

        self.clients = []
        if not self.server.listen(port=self.port):
            self.tcpmodelError.emit()
        else:
            self.server.newConnection.connect(self.__new_connection)


    def initialize(self):
        pass

    def __new_connection(self):
        
        self.client_connection = self.server.nextPendingConnection()
        self.client_connection.readyRead.connect(self.__receive_message)
        self.client_connection.disconnected.connect(self.client_connection.deleteLater)
        self.clients.append(self.client_connection)
        
    def __receive_message(self):
    
        if self.client_connection.bytesAvailable()>0:
            message = self.client_connection.readAll().data().decode()
            
            self.messageReceived.emit(message)
            
    
    def send_message(self, message):
        
        for client_socket in self.clients:
            client_socket.write(QByteArray(message.encode()))
        # if self.client_connection.isOpen():
        #     self.client_connection.write(message.encode())
        #     print("server sent a message")
        # print("server didn't sent a message - no client connection")


class Client(QObject):
    messageReceived = pyqtSignal(str)
    tcpmodelError = pyqtSignal()
    def __init__(self, ports, parent=None):
        super().__init__()
        self.port = ports
        self.parent = parent
        self.isConnected = False
        self.__init_client()

    
    def __init_client(self):
        
        self.client = QTcpSocket(self)
        
       
    def initialize(self):
        self.connect_to_server()
       
    def connect_to_server(self):
        self.client.connectToHost('127.0.0.1', self.port)
        self.client.readyRead.connect(self.__receive_message)
        self.client.errorOccurred.connect(self.tcpmodelError)
        self.client.disconnected.connect(lambda: print("Disconnected from the server"))
        
        self.isConnected = True

    def __receive_message(self):
        if self.client.bytesAvailable():
            message = self.client.readAll().data().decode()
            
            self.messageReceived.emit(message)


    def send_message(self, message):
        if not self.isConnected:
            self.connect_to_server()
        #if self.client.state() == QAbstractSocket.SocketState.ConnectedState:
        self.client.write(QByteArray(message.encode()))
       
