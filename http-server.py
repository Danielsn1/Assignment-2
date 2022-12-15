import socket
import threading
import os
import sys
import datetime

#CONSTANTS
SERVER_IP = socket.gethostbyname(socket.gethostname())
PORT = 8081
ADDR = (SERVER_IP, PORT)
LEN_MESSAGE = 2**13
FORMAT = 'utf-8'
HTTP_VERSION = "HTTP/1.1"
VALID_METHODS = ['GET', 'PUT', 'HEAD', 'POST', 'DELETE']

#METHODS
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
    #for

    return (request, header_lines)
#parse_header()


def start(socket: socket.socket) -> None:
    socket.listen(5)
    
    while True:
        conn, addr = socket.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
    # while
# start()


def valid_request(request: str) -> bool | str:
    '''
    Takes in a http request and determines whether all of the aspects of the request are
    valid, whether the version is supported, and whether the method defined is a valid method.
    If the request is not valid the correct error code tobe sent is returned
    '''
    method, _ , version = request.split(maxsplit=2)
    if method not in VALID_METHODS:
        return '400'
    elif not version == HTTP_VERSION:
        return '505'
    else:
        return True
# valid_request()


def handle_client(conn, addr) -> None:
    print("[NEW CONNECTION] address ", addr)

    # reads first 8KB from the socket
    initial_message = conn.recv(LEN_MESSAGE)

    # checks if the header exceeds the 8KB limit and sends a bad request error
    # if it is found that it does exceed the limit
    if b'\n\n' not in initial_message:
        responses('400', conn)
    #if

    # gets the header and any of the body that was within the first 8KB read.
    header, partial_message = initial_message.split(b'\n\n', 1)

    request, header_lines = parse_header(header)

    # checks if the request is valid and if it is not saves the code returned so that 
    # the correct error message can be sent
    if ((code := valid_request(request)) is True):
        # checks if content lenght is defined denoting the existance of a body
        if ((content_length := int(header_lines.get('Content-Length', -1))) != -1):
            # Gathers the type of the content being sent
            if (content_type := header_lines['Content-Type']):
                # checks if the entire body was read within the first 8KB
                if (len(partial_message) < content_length):
                    # if body was not read within first 8KB the rest of the body is
                    # read and joined with existing portion of the body
                    message = partial_message +conn.recv(
                        content_length - len(partial_message))
                else:
                    message = partial_message
                # if/else
            else:
                responses('400', conn)
            #if/else
        #if

        method, url, _ = request.split(maxsplit=2)

        if method == 'GET':
            potential_file = os.path.join(
                os.path.dirname(__file__), url.replace('/', '', 1))

            if not os.path.exists(potential_file):
                responses('404', conn)
            else:
                print("[Selected File]: ", potential_file)
                with open(potential_file, 'rb') as f:
                    contents = f.read()
                responses('200', conn, entity_body=contents)
            #if/else

        elif method == "POST":
            post_file = os.path.join(
                os.path.dirname(__file__), 'post-requests.txt')
            with open(post_file, 'ab') as f:
                f.write(message + b'\n')
            responses('200', conn)
            

        elif method == "HEAD":
            potential_file = os.path.join(
                os.path.dirname(__file__), url.replace('/', '', 1))

            if not os.path.exists(potential_file):
                responses('404', conn)
            else:
                print("[Selected File]: ", potential_file)
                with open(potential_file, 'rb') as f:
                    contents = f.read()
                responses('200', conn, entity_body=contents, head=True)
            #if/else

        elif method == "PUT":
            pass
            # potential_file = os.join(os.path.dirname(__file__), url)

            # if not os.path.exists(potential_file):
            #     head_tail = os.path.split(potential_file)
            #     tail = head_tail[1]
            #     f = open(tail, "x")
            #     f.write(message)
            #     f.close()
            #     responses('200', conn)
            # else:
            #     head_tail = os.path.split(potential_file)
            #     tail = head_tail[1]
            #     f = open(tail, 'w')
            #     f.write(message)
            #     f.close()
            #     responses('200', conn)
            # if/else

        elif method == "DELETE":
            potential_file = os.path.join(
                os.path.dirname(__file__), url.replace('/', '', 1))

            if not os.path.exists(potential_file):
                responses('404', conn)
            else:
                print("[Selected File]: ", potential_file)
                os.remove(potential_file)
                responses('200', conn)
            #if/else
        #if/else
    else:
        responses(code,conn)
    #if/else
#handle_client()


def responses(code, conn, entity_body=None, head=False) -> None:
    dt = datetime.datetime.now()

    # if the body is not bytes it is converted to bytes at this point
    if not isinstance(entity_body, bytes):
        if entity_body is None:
            entity_body = b''
        else:
            entity_body = entity_body.encode(FORMAT)

    if code == "200":
        status_line = HTTP_VERSION + ' ' + code + " OK" + "\n"
        header_lines = "Connection: close " + "\n" + "Date: " + str(dt) + " CST \n" + \
            "Server: " + "Fredrick " + "(" + sys.platform + ") \n"
            
        if entity_body is not None:
            header_lines += "Content-Length: " + str(len(entity_body)) + '\n' + \
                "Content-Type: text/text" + '\n'
        #if
        
        response_message = status_line + header_lines + '\n'
        response_message = response_message.encode(FORMAT)

        if head is not True:
            response_message = response_message + entity_body

        conn.send(response_message)

    elif code == "404":
        status_line = HTTP_VERSION + ' ' + code + " Not Found" + "\n"
        header_lines = "Connection: close " + "\n" + "Date: " + str(dt) + " CST \n" + \
            "Server: " + "Fredrick " + "(" + sys.platform + ") \n"
        response_message = (status_line + header_lines + '\n').encode(FORMAT) + entity_body
        conn.send(response_message)

    elif code == "505":
        status_line = HTTP_VERSION + ' ' + code + " HTTP Version Not Supported" + "\n"
        entity_body = b'The HTTP version you are asking for is unsupported '
        header_lines = "Connection: close " + "\n" + "Date: " + str(dt) + " CST \n" + \
            "Server: " + "Fredrick " + "(" + sys.platform + ") \n" + \
            "Content-Length: " + str(len(entity_body)) + '\n' + \
            "Content-Type: text/text" + '\n'
        response_message = (status_line + header_lines + '\n').encode(FORMAT) + entity_body
        conn.send(response_message)

    elif code == '400':
        status_line = HTTP_VERSION + ' ' + code + " Bad Request" + "\n"
        header_lines = "Connection: close " + "\n" + "Date: " + str(dt) + " CST \n" + \
            "Server: " + "Fredrick " + "(" + sys.platform + ") \n" + \
            "Content-Length: " + str(len(entity_body)) + '\n' + \
            "Content-Type: text/text" + '\n'
        response_message = (status_line + header_lines + '\n').encode(FORMAT) + entity_body
        conn.send(response_message)
    #if/else

    conn.close()
    print("[CONNECTION CLOSE]")
#responses()

def send_all(response_message, conn):
    length = len(response_message) + 1
    sent_bytes = 0 
    while length < sent_bytes:
        sent_bytes += conn.send(response_message)
    else: 
        print("All Bytes Sent")
#send_all()



#MAIN
if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(ADDR)
    start(server_socket)
#main()
