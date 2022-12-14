import socket

# variables
HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'
SERVER_PORT = 8081

# methods


def send_message(msg, client_socket):
    message = msg.encode(FORMAT)

    length = len(message)
    length = str(length).encode(FORMAT)

    length += b' ' * (HEADER - len(length))

    client_socket.send(length)
    client_socket.send(message)
# send_message


def start_client():
    SERVER_IP = "10.103.65.12"
    SERVER_ADDR = (SERVER_IP, SERVER_PORT)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(SERVER_ADDR)

    msg = input("Enter message (Type quit to exit): ")

    while msg != "quit":
        send_message(msg, client_socket)
        msg = input("Enter message (Type quit to exit): ")
    else:  # hehe i use troll python while/else
        send_message(DISCONNECT_MESSAGE, client_socket)
        client_socket.close()
    # while/else
# start_client


# main
start_client()
