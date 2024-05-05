from forms.tcpModel import Server, Client
from PyQt6.QtWidgets import QApplication
import sys
import time

if __name__ == '__main__':
    app = QApplication(sys.argv)
    server = Server(5000)
    client = Client(5000)

    client.messageReceived.connect(lambda msg: print("Client received: ", msg))
    #server.messageReceived.connect(lambda msg: print(f"Server received: {msg}"))

    client.connect_to_server()
    client.send_message("start_message")


    time.sleep(2)

    server.send_message("Hello")


    sys.exit(app.exec())
