import socket
import pandas as pd
import config

# THIS IS ON D 2
print(socket.gethostbyname(socket.gethostname()))
HEADER = 64
PORT = 5070
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = config.LAPTOP_IP  # Needs static IP
ADDRESS = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print("Sent:\n" + msg)
    return client.recv(5000).decode(FORMAT)


def data_response(msg):
    info = msg[1:].split(">", 1)
    data = info[1]
    if data[-4:] == config.COMM_PROC["end_token"]:
        data = data[:-4]
    else:
        response = data
        while True:
            if response[-4:] == config.COMM_PROC["end_token"]:
                data += response[:-4]
                break
            response = client.recv(5000).decode(FORMAT)
            data += response

    print(len(data))
    text_file = open(info[0], "w")
    a = text_file.write(data)
    text_file.close()


def read_commands():
    print("nice")


message = send("get_whole_database(\"" + config.COMMANDS_CSV[:-4] + "\")")
eval(config.COMM_PROC[message[:4]])

message = send("get_commands()")
eval(config.COMM_PROC[message[:4]])


