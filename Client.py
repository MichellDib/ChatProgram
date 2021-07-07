import socket
import threading
from typing import Text
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QInputDialog, QLineEdit, QPlainTextEdit, QStackedLayout, QStackedWidget, QDialog, QApplication, QTextBrowser, QWidget
from PyQt5 import QtWidgets
import sys
import time

HEADER = 64
PORT = 6969
FORMAT = 'utf-8'
DC_CMD = "!DISCONNECT"
IP = "193.180.165.181"
ADDR = (IP,PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
Messages = []

class chat_window(QDialog):
    """A class used to represent the application window.
    
    Methods:
        disconnect()
            Disconnects and closes the application.

        send_from_lineEdit()
            Sends the message that has been written into
            the line editor.
        
        display_message(String)
            Displays String in text editor.
    """

    def __init__(self):
        super(chat_window, self).__init__()
        loadUi("chat_window.ui", self)

        # Calls disconnect method on 'disconnect_button' click.
        self.disconnect_button.clicked.connect(self.disconnect)

        # Calls send_from_lineEdit method on 'send_button' click.
        self.send_button.clicked.connect(self.send_from_lineEdit)
        
    def disconnect(self):
        send("!DISCONNECT")
        time.sleep(1)
        client.close()
        sys.exit()

    def send_from_lineEdit(self):
        message = self.message_input.text()
        send(message)
        self.message_input.clear()

    def display_message(self, msg):
        self.textEditor.setReadOnly(True)
        self.textEditor.insertPlainText(msg + "\n")

def send(msg):
    """
    Sends message to server.

    Encodes the parameter using utf-8 formatting,
    then sends encoded message to server.

    Args:
        msg: String containing the message to be sent.
    """

    message = msg.encode(FORMAT)
    msg_len = len(message)
    send_len = str(msg_len).encode(FORMAT)
    send_len += b' ' * (HEADER - len(send_len))
    client.send(send_len)
    client.send(message)

def recieve():
    """
    Recieves, decodes and prints messages from the server.
    If message is equal to the disconnect command, 
    the function will stop.
    """

    while 1:
            msg_len = client.recv(HEADER).decode(FORMAT)
            if msg_len:
                msg_len = int(msg_len)
                msg = client.recv(msg_len).decode(FORMAT)
                if msg == DC_CMD:
                    break
                if msg != "":
                    chat.display_message(msg)

# Initialization of application window.
app = QApplication(sys.argv)
chat = chat_window()
widget = QtWidgets.QStackedWidget()
widget.addWidget(chat)
widget.setWindowTitle('Michells Chatroom :)')

def main():
    """Handles inputting of messages and the start of the recieve function."""

    widget.show()
    try:
        sys.exit(app.exec)
    except:
        "Exiting"
    thread = threading.Thread(target=recieve, args=())
    thread.start()
    input()
main()
        
    