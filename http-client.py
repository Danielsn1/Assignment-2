import socket
import os

#CONSTANTS
FORMAT = 'utf-8'
QUIT_PROMPT = 'quit'
SERVER_PORT = 8081
LEN_MESSAGE = 2**12
HTTP_VERSION = "HTTP/1.1"

#METHODS
def send_all(response_message: bytes, conn: socket.socket) -> None:
    length = len(response_message)
    sent_bytes = 0 
    
    while sent_bytes < length:
        sent_bytes += conn.send(response_message[sent_bytes:])
#send_all()


def get_request(host: str, uri: str) -> bytes:
    request_line = "GET " + uri + " " + HTTP_VERSION + "\n"
    header_lines = "Host: " + host + "\nConnection: close\n"

    return (request_line + header_lines + '\n').encode(FORMAT)
#get_reqeust()


def post_request(host: str, uri: str, msg: str) -> bytes:
    request_line = "POST " + uri + " " + HTTP_VERSION + "\n"
    header_lines = "Host: " + host + "\n" +\
        "Connection: close\n" +\
        "Content-Length: " + str(len(msg.encode(FORMAT))) + "\n" +\
        "Content-Type: text/text\n"

    return (request_line + header_lines + '\n' + msg).encode(FORMAT)
#post_reqeust()


def put_request(host: str, uri: str, msg: str) -> bytes:
    request_line = "PUT " + uri + " " + HTTP_VERSION + "\n"
    header_lines = "Host: " + host + "\n" +\
        "Connection: close\n" +\
        "Content-Length: " + str(len(msg)) + "\n" +\
        "Content-Type: text/text\n"

    return (request_line + header_lines + '\n').encode(FORMAT) + msg
#put_reqeust()


def delete_request(host: str, uri: str) -> bytes:
    request_line = "DELETE " + uri + " " + HTTP_VERSION + "\n"
    header_lines = "Host: " + host + "\n" +\
        "Connection: close\n"

    return (request_line + header_lines + '\n').encode(FORMAT)
#delete_reqeust()


def head_request(host: str, uri: str) -> bytes:
    request_line = "HEAD " + uri + " " + HTTP_VERSION + "\n"
    header_lines = "Host: " + host + "\n" +\
        "Connection: close\n"

    return (request_line + header_lines + '\n').encode(FORMAT)
#head_reqeust()


def request(method: str, host: str, uri: str, msg: str = None) -> None:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, SERVER_PORT))

    if method == 'GET':
        send_all(get_request(host, uri), client_socket)
    elif method == 'POST':
        send_all(post_request(host, uri, msg), client_socket)
    elif method == 'PUT':
        send_all(put_request(host, uri, msg), client_socket)
    elif method == 'DELETE':
        send_all(delete_request(host, uri), client_socket)
    elif method == 'HEAD':
        send_all(head_request(host, uri), client_socket)
    #if/else

    # reads first 4KB from the socket
    initial_message = client_socket.recv(LEN_MESSAGE)

    # reads in header information 4KB at a time
    while b'\n\n' not in initial_message:
        initial_message += client_socket.recv(LEN_MESSAGE)
    #while

    # gets the header and any of the body that was within the first 8KB read.
    header, partial_message = initial_message.split(b'\n\n', 1)

    response, header_lines = parse_header(header)

    message = None

    # checks if content lenght is defined denoting the existance of a body
    if (content_length := int(header_lines.get('Content-Length', -1))) != -1:
        # Gathers the type of the content being sent
        content_type = header_lines['Content-Type']
        
        # checks if the entire body was read within the first 4KB
        if (len(partial_message) < content_length):
            # if body was not read within first 8KB the rest of the body is
            # read and joined with existing portion of the body
            message = partial_message + client_socket.recv(
                content_length - len(partial_message)) 
        else:
            message = partial_message
        #if/else
    #if
    
    client_socket.close()
    
    print('\n' + response)
    
    if message is not None:
        print(message.decode(FORMAT))
    #if

    if method == 'GET' and response.split()[1] == "200":
        with open(os.path.split(uri)[1], 'wb') as f:
            f.write(message)
    #if
    
    print()
#request()


def parse_header(header: bytes) -> tuple[str, dict]:
    '''
    This function takes in an http header and returns the request along with all of the 
    key value header lines
    '''

    header = header.decode(FORMAT).split('\n')

    response = header.pop(0)

    header_lines = {}
    for field in header:
        # creates key and value pair from the header lines and stores them in the dictionary
        key, value = field.split(': ', 1)
        header_lines[key] = value

    return (response, header_lines)
#parse_header()


def start_client() -> None:
    msg = ""
    msg_uri = ""
    msg_type = ""
    host = ""

    print("Enter Numerical Code for Desired HTTP Message Type")

    while (True):
        msg_type = input("Options:\n1:GET \n2:POST \n3:PUT \n4:DELETE \n5:HEAD\n(or " +
                         QUIT_PROMPT + " to exit)  :\n")

        # this is temperary until the next assignment when we fully impliment put
        if (msg_type == '3'):
            print('This method is currently not implimented\n')
            continue
        
        if (msg_type == QUIT_PROMPT):
            break
        #if

        host = input("Enter server address (or " +
                     QUIT_PROMPT + " to exit)  :\n")

        if (host == QUIT_PROMPT):
            break
        #if

        msg_uri = input("Enter HTTP Request URI  :\n")

        if (msg_uri == QUIT_PROMPT):
            break
        #if

        if (msg_type == '1'):
            request('GET', host, msg_uri)

        elif (msg_type == '2'):
            msg = input(
                "Enter Data to be sent to given URI (or " + QUIT_PROMPT + " to exit)  :\n")

            if (msg == QUIT_PROMPT):
                break
            #if

            request('POST', host, msg_uri, msg)

        # this code will not execute
        elif (msg_type == '3'):
            msg = input(
                "Select File to be created at given URI (or " + QUIT_PROMPT + " to exit)  :\n")

            if (msg == QUIT_PROMPT):
                break
            #if

            request('PUT', host, msg_uri, msg)

        elif (msg_type == '4'):
            request('DELETE', host, msg_uri)

        elif (msg_type == '5'):
            request('HEAD', host, msg_uri)

        else:
            print("Enter Numerical Code for Desired HTTP Message Type")  
        #if/else
    #while
#start_client()


#MAIN
if __name__ == '__main__':
    start_client()
#main()
