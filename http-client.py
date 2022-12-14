import socket

#variables
HEADER = 64
FORMAT = 'utf-8'
QUIT_PROMPT = "quit"
DISCONNECT_MESSAGE = '!DISCONNECT'
SERVER_PORT = 8081


#methods
def send_message(msg, client_socket):
  message = msg.encode(FORMAT)
  
  length = len(message)
  length = str(length).encode(FORMAT)
  
  length += b' ' * (HEADER - len(length))
  
  client_socket.send(length)
  client_socket.send(message)
#send_message

def get_request(uri):
  return
#get_reqeust

def post_request(uri, msg):
  return
#post_reqeust

def put_request(uri, msg):
  return
#put_reqeust

def start_client():
  temp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  temp_socket.connect(("ip, port"))
  #HEY I DID NOT FINISH THAT LAST LINE
  SERVER_IP = temp_socket.getsockname()[0]
  temp_socket.close
  SERVER_ADDR = (SERVER_IP, SERVER_PORT)
  
  client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client_socket.connect(SERVER_ADDR)

  msg = ""
  msg_uri = ""
  msg_type = ""
  
  while (msg != QUIT_PROMPT and msg_type != QUIT_PROMPT and msg_uri != QUIT_PROMPT):
    
    print("Enter Code for Desired HTTP Message Type (or "+ QUIT_PROMPT + " to exit)")
    msg_type = input("Options: 1:GET, 2:POST, 3:PUT  :")
    
    if (msg_type = QUIT_PROMPT):
      break
    #if
    
    msg_uri = input("Enter HTTP Request URI"  :)
    
    if (msg_uri = QUIT_PROMPT):
      break
    #if
    
    if (msg_type == 1):
      
      #get_request(msg_uri)
      
    elif (msg_type == 2):
      
      msg = input("Enter Data to be sent to given URI (or "+ QUIT_PROMPT + " to exit)  :")
      
      if (msg = QUIT_PROMPT):
        break
      #if
      
      #post_request(msg_uri, msg)
      
    elif (msg_type == 3):
      
      msg = input("Select File to be created at given URI (or "+ QUIT_PROMPT + " to exit)  :")
      
      if (msg = QUIT_PROMPT):
        break
      #if
      
      #put_request(msg_uri, msg)
      
    else:
      
      print("Improper Message Format: HTTP Message Type Code Not Recognized")
      break
      
    #if/else
    
    #send_message(msg, client_socket)
    
  else: #hehe i use troll python while/else
    
    send_message(msg, client_socket)
    client_socket.close()
    print("EXIT")
    
  #while/else
#start_client

#main
start_client()
