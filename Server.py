import socket
import threading

HEADER = 64
PORT = 6969
SERVER = "193.180.165.181"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DC_CMD = "!DISCONNECT"
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
Clients = []

"""
Client class that defines a Client. Each Client
has a connection and an address (Consisting of IP and PORT).
"""
class Client:
    # Constructor for Client class
    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
    
    # Getter method for the clients address
    def addr(self):
        return self.addr

    # Getter method for the clients connection
    def conn(self):
        return self.conn

def client_handler(conn, addr):
    """ Handles each Client.

    Handles the chat and manages the commands that 
    are available to the clients.
    It recieves all messages, handles disconnects, 
    and redistributes the messages.

    Args: 
        conn: The established connection to the client.
        addr: Contains the address (IP, PORT) for the client.
    """
    print(f"[New connection] {addr}")
    connected = True

    # Loop that runs while connected, 
    # once loop is done, the connection will close.
    while connected:
        msg_len = conn.recv(HEADER).decode(FORMAT)

        # If a message is recieved from client, 
        # extract message length and decode 
        # using utf-8 format.
        if msg_len:
            msg_len = int(msg_len)
            msg = conn.recv(msg_len).decode(FORMAT)

            if msg == DC_CMD:
                connected = False
                send(msg, addr)

                # Algorithm that gives the recipient information
                # about how large the message is,
                # and decides on a byte-size equal to the 
                # size of the message for the recv method.
                msg = msg.encode(FORMAT)
                msg_len = len(msg)
                send_len = str(msg_len).encode(FORMAT)
                send_len += b' ' * (HEADER - len(send_len))

                # Stops the recieve thread for the client,
                # to properly close the program.
                conn.send(send_len)
                conn.send(msg)

                # Disconnects client, and removes
                # them from "Clients" list.
                for Client in Clients:
                    if Client.conn == conn:
                        Client.conn.close()
                        Clients.remove(Client)
                        break

                print(f"[{addr}] has disconnected.")
                continue

            # If the message is not disconnect command nor 
            # empty, send.
            if msg != "":
                print(f"[{addr}]: {msg}")
                send(msg, addr)
    conn.close()


def start_up():
    """
    Listens and accepts connections, creates new clients and stores
    them in Clients list. Starts new instance of client handler 
    function for each client, using threads.
    """
    server.listen()
    print("Server is listening...")
    while True:
        conn, addr = server.accept()
        Clients.append(Client(conn, addr))
        thread = threading.Thread(target=client_handler, args=(conn, addr))
        thread.start()


def send(msg, addr):
    """Sends message to all clients.

    Sends a message to all clients, depending on if the 
    message is equal to the disconnect command. Either
    a "X has disconnected" message is sent, or just the
    intended message.

    Args: 
        msg: A string containing the message being sent.
        addr: Address for the sender sending the message.
    """
    # If message equals disconnect command,
    # change message to "system output"-like command.
    if msg == DC_CMD:
        msg = (f"[{addr}] has disconnected.")

    else: 
        msg = (f"[{addr}]: {msg}")

    # Encode
    message = msg.encode(FORMAT)
    msg_len = len(message)
    send_len = str(msg_len).encode(FORMAT)
    send_len += b' ' * (HEADER - len(send_len))

    # Distributes the message as a string to all
    # Clients in the Clients list.
    for Client in Clients:
        Client.conn.send(send_len)
        Client.conn.send(message)

print("SERVER STARTING...")
start_up()