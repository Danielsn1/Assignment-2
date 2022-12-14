import socket
import os

# variables
HEADER = 64
FORMAT = 'utf-8'
QUIT_PROMPT = 'quit'
DISCONNECT_MESSAGE = '!DISCONNECT'
SERVER_PORT = 8081
LEN_MESSAGE = 2**14
HTTP_VERSION = "HTTP/1.1"


# methods
def get_request(host, uri):
    request_line = "GET " + uri + " " + HTTP_VERSION + "\n"
    header_lines = "Host: " + host + "\nConnection: close\n"

    return (request_line + header_lines + '\n').encode(FORMAT)
# get_reqeust()


def post_request(host, uri, msg):
    request_line = "POST " + uri + " " + HTTP_VERSION + "\n"
    header_lines = "Host: " + host + "\n" +\
        "Connection: close\n" +\
        "Content-Length: " + len(msg.encode(FORMAT)) + "\n" +\
        "Content-Type: text/text\n"

    return (request_line + header_lines + '\n' + msg).encode(FORMAT)
# post_reqeust()


def put_request(host, uri, msg):
    request_line = "PUT " + uri + " " + HTTP_VERSION + "\n"
    header_lines = "Host: " + host + "\n" +\
        "Connection: close\n" +\
        "Content-Length: " + len(msg) + "\n" +\
        "Content-Type: text/text\n"

    return (request_line + header_lines + '\n').encode(FORMAT) + msg
# put_reqeust()


def delete_request(host, uri):
    request_line = "DELETE " + uri + " " + HTTP_VERSION + "\n"
    header_lines = "Host: " + host + "\n" +\
        "Connection: close\n"

    return (request_line + header_lines + '\n').encode(FORMAT)
# delete_reqeust()


def head_request(host, uri):
    request_line = "HEAD " + uri + " " + HTTP_VERSION + "\n"
    header_lines = "Host: " + host + "\n" +\
        "Connection: close\n"

    return (request_line + header_lines + '\n').encode(FORMAT)
# head_reqeust()


def request(method: str, host: str, uri: str, msg: str = None):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, SERVER_PORT))

    if method == 'GET':
        client_socket.send(get_request(host, uri))
    elif method == 'POST':
        client_socket.send(post_request(host, uri, msg))
    elif method == 'PUT':
        client_socket.send(put_request(host, uri, msg))
    elif method == 'DELETE':
        client_socket.send(delete_request(host, uri))
    elif method == 'HEAD':
        client_socket.send(head_request(host, uri))
    # if/else

    # reads first 8KB from the socket
    initial_message = client_socket.recv(LEN_MESSAGE)

    # reads in header information 4KB at a time
    while b'\n\n' not in initial_message:
        initial_message = client_socket.recv(LEN_MESSAGE)
    # while

    # gets the header and any of the body that was within the first 8KB read.
    header, partial_message = initial_message.split(b'\n\n', 1)

    response, header_lines = parse_header(header)

    print(response, header_lines, sep='\n')

    message = None

    # checks if content lenght is defined denoting the existance of a body
    if (content_length := int(header_lines.get('Content-Length'))):
        # Gathers the type of the content being sent
        content_type = header_lines['Content-Type']
        print(len(partial_message))
        # checks if the entire body was read within the first 8KB
        if (len(partial_message) < content_length):
            # if body was not read within first 8KB the rest of the body is
            # read and joined with existing portion of the body
            message = bytes.join([partial_message, client_socket.recv(
                content_length - len(partial_message))])
        else:
            message = partial_message
            # if/else
        # if
    # if

    if response.split()[1] == "200":
        print(response, message.decode(FORMAT), sep='\n')

    if method == 'GET' and response.split()[1] == "200":
        with open(os.path.split(uri)[1], 'wb') as f:
            f.write(message)
    # if
    # request()


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
# parse_header()


def start_client():
    msg = ""
    msg_uri = ""
    msg_type = ""
    host = ""

    print("Enter Numerical Code for Desired HTTP Message Type")

    while (True):
        msg_type = input("Options:\n1:GET \n2:POST \n3:PUT \n4:DELETE \n5:HEAD\n(or " +
                         QUIT_PROMPT + " to exit)  :\n")

        if (msg_type == QUIT_PROMPT):
            break
        # if

        host = input("Enter server address (or " +
                     QUIT_PROMPT + " to exit)  :\n")

        if (host == QUIT_PROMPT):
            break
        # if

        msg_uri = input("Enter HTTP Request URI  :\n")

        if (msg_uri == QUIT_PROMPT):
            break
        # if

        if (msg_type == '1'):
            request('GET', host, msg_uri)

        elif (msg_type == '2'):
            msg = input(
                "Enter Data to be sent to given URI (or " + QUIT_PROMPT + " to exit)  :\n")

            if (msg == QUIT_PROMPT):
                break
            # if

            request('POST', host, msg_uri, msg)

        elif (msg_type == '3'):
            msg = input(
                "Select File to be created at given URI (or " + QUIT_PROMPT + " to exit)  :\n")

            if (msg == QUIT_PROMPT):
                break
            # if

            request('PUT', host, msg_uri, msg)

        elif (msg_type == '4'):
            request('DELETE', host, msg_uri)

        elif (msg_type == '5'):
            request('HEAD', host, msg_uri)

        else:
            print("Improper Message Format: HTTP Message Type Code Not Recognized")
            print("Enter Numerical Code for Desired HTTP Message Type")
        # if/else
    # while
# start_client()


# main
if __name__ == '__main__':
    start_client()
# main()
