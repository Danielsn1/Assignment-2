import socket
import threading
import os

#temp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#temp_socket.connect(("8.8.8.8", 53))
# temp_socket.getsockname()[0]
# temp_socket.close()

# Consts
SERVER_IP = socket.gethostbyname(socket.gethostname())
PORT = 8081
ADDR = (SERVER_IP, PORT)
LEN_MESSAGE = 2**13
FORMAT = 'utf-8'
HTTP_VERSION = "1.1"
VALID_METHODS = ['GET', 'PUT', 'HEAD', 'POST', 'DELETE']

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(ADDR)


def parse_header(header: bytes) -> tuple[str, dict]:
    '''
    This function takes in an http header and returns the request along with all of the 
    key value header lines
    '''

    header = header.decode(FORMAT).split('\n')

    request = header.pop(0)

    header_lines = {}
    for field in header:
        # creates key and value pair from the header lines and stores them in the dictionary
        key, value = field.split(': ', 1)
        header_lines[key] = value

    return (request, header_lines)


def start():
    server_socket.listen(5)
    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


def valid_url(url: str) -> bool:
    '''
    Takes in a http url and determines whether or not it is a valid url
    '''
    return True


def valid_request(request: str) -> bool:
    '''
    Takes in a http request and determines whether all of the aspects of the request are
    valid, whether the version is supported, whether the url given is valid, and whether 
    the method defined is a valid method
    '''
    method, url, version = request.split(maxsplit=2)
    return method in VALID_METHODS and valid_url(url) and version == HTTP_VERSION


def handle_client(conn, addr):
    print("[NEW CONNECTION] address ", addr)

    # reads first 8KB from the socket
    initial_message = conn.recv(LEN_MESSAGE).decode(FORMAT)

    # checks if the header exceeds the 8KB limit and sends a bad request error
    # if it is found that it does exceed the limit
    if b'\n\n' not in initial_message:
        responses(400, conn)

    # gets the header and any of the body that was within the first 8KB read.
    header, partial_message = initial_message.split(b'\n\n', 1)

    request, header_lines = parse_header(header)

    if (not valid_request(request)):
        responses(400, conn)

    # checks if content lenght is defined denoting the existance of a body
    if (content_length := header_lines.get('Content-Length')):
        # Gathers the type of the content being sent
        if (content_type := header_lines['Content-Type']):
            print(len(partial_message))
            # checks if the entire body was read within the first 8KB
            if (len(partial_message) < content_length):
                # if body was not read within first 8KB the rest of the body is
                # read and joined with existing portion of the body
                message = bytes.join([partial_message, conn.recv(
                    content_length - len(partial_message))])
            else:
                message = partial_message
        else:
            responses(400, conn)

    if filename != None:

        file_dir = find_files(filename, os.path.dirname(__file__))

        if file_dir == []:
            responces(400, conn)
        else:
            print("selected file: ", filename)
            with open(file_dir, 'rb') as f:
                contents = f.read()
            responces(200, conn, body=contents)
    else:
        responces(200, conn, body="hello")

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


def responses(code, conn, body=None):
    if code == "200":
        conn.send(body)
        conn.close
    if code == "404":
        conn.send('Error 404')
        conn.close()
    if code == "505":
        pass


def find_files(filename, search_path):
    result = []
    for root, dir, files in os.walk(search_path):
        if filename in files:
            result.append(os.path.join(root, filename))
    return result


start()
