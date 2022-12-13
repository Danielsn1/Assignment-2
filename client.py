import socket

#variables
HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'
SERVER_PORT = 8081

#methods
def send_message(msg, client_socket):
  message = msg.encode(FORMAT)
  
  length = len(message)
  length = str(length).encode(FORMAT)
  
  length += b' ' * (HEADER - len(length))
  
  client_socket(length)
  client_socket(message)
#send_message

def start_client():
  temp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  temp_socket.connect(("ip, port"))
  #HEY I DID NOT FINISH THAT LAST LINE
  SERVER_IP = temp_socket.getsockname()[0]
  temp_socket.close
  SERVER_ADDR = (SERVER_IP, SERVER_PORT)
  
  client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client_socket.connect(SERVER_ADDR)
  
  msg = input("Enter message (Type quit to exit): ")
  
  while msg != "quit":
    send_message(msg, client_socket)
    msg = input("Enter message (Type quit to exit): ")
  else: #hehe i use troll python while/else
    send_message(msg, client_socket)
    client_socket.close()
  #while/else
#start_client

#main
start_client()
