import socket
import threading

PORT = 8081
SERVER_IP = socket.gethostbyname(socket.gethostname())
print(SERVER_IP)
ADDR = (SERVER_IP, PORT)
LEN_MESSAGE = 64
FORMAT = 'utf-8'
DISSCONNECT_MESSAGE = "!DISCONNECT"

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(ADDR)


def start():
    server_socket.listen(5)
    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


def handle_client(conn, addr):
    print("[new connection!] address", addr)

    connected = True

    while connected:
        msg_length = conn.recv(LEN_MESSAGE).decode(FORMAT)
        if msg_length:
            length_of_message = int(msg_length)
            print("[MESSAGE LENGTH]", length_of_message)
            message = conn.recv(length_of_message).decode(FORMAT)
            print("[MESSAGE]", message)

            if message == DISSCONNECT_MESSAGE:
                connected = False
    print("[CONNECTION CLOSE] Addr: ", addr)
    conn.close()


start()
