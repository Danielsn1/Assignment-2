import socket
import threading

temp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
temp_socket.connect(("8.8.8.8", 53))

SERVER_IP = temp_socket.getsockname()[0]
temp_socket.close()

#Consts
PORT = 8081
ADDR = (SERVER_IP, PORT)
LEN_MESSAGE = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(ADDR)

def start():
    server_socket.listen(5)
    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        
def handle_client(conn, addr):
    print("[NEW CONNECTION] address ", addr)
    msg_length = conn.recv(LEN_MESSAGE).decode(FORMAT)
    
    connected = True
    
    while connected:
        if msg_length:
            length_of_message = int(msg_length)
            print("[MESSAGE LENGTH] ", length_of_message)
            message = conn.recv(length_of_message).decode(FORMAT)
            print("[MESSAGE] ", message)
            
            if message == DISCONNECT_MESSAGE:
                connected = False
    
    print("[CONNECTION CLOSE] Addr: ", addr)
    conn.close()
start()