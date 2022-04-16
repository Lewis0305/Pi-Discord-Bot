import socket
import threading
import pandas as pd

# THIS IS ON THE PI
HEADER = 64
PORT = 5070
SERVER = socket.gethostbyname(socket.gethostname())  # Finds a IP it likes (can be a string of ip)
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(ADDR)

video_database = pd.read_csv('broadcasters.csv', index_col=0)


def get_whole_database(csv):
    text = open(csv, "r")
    text = ''.join([i for i in text])
    return str("<!d>" + "<broadcasters2.csv>" + text + "<!e>")


def get_commands():
    return "<!c>none atm<!e>"


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                conn.send("Successful Disconnected".encode(FORMAT))
                break

            print(f"[{addr}] {msg}")
            response = eval(msg)
            conn.send(response.encode(FORMAT))

    conn.close()


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()

"""
import socket

# take the server name and port name

host = 'local host'
port = 5000

# create a socket at client side
# using TCP / IP protocol
s = socket.socket(socket.AF_INET,
                  socket.SOCK_STREAM)

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# connect it to server and port
# number on local computer.
# s.connect(('192.168.1.2', port))
s.connect(('192.168.1.17', port))

# receive message string from
# server, at a time 1024 B
msg = s.recv(1024)

# repeat as long as message
# string are not empty
while msg:
    print('Received::' + msg.decode())
    msg = s.recv(1024)

# disconnect the client
s.close()
"""