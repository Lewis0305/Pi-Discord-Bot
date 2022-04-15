# from wakeonlan import send_magic_packet
# send_magic_packet('D0-50-99-A7-88-AE')
# send_magic_packet('4C.CC.6A.2E.3C.94')
# send_magic_packet('9C.B6.D0.09.A8.EB')
# send_magic_packet('9E.B6.D0.09.A8.EB')
# send_magic_packet('AE.B6.D0.09.A8.EB')
# send_magic_packet('9C.B6.D0.09.A8.EC')

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
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print("Sent:\n" + msg)
    # TODO This can only send 5000 rows (Should only add new entries (requires change to the file write))
    # TODO Only New Entry method will not account for modified rows
    return client.recv(5000).decode(FORMAT)


def data_response(msg, csv):
    response = msg
    data = response[4:]
    if response[-4:] == "<!e>":
        data = data[:-4]
    else:
        while True:
            if response[-4:] == "<!e>":
                data += response[:-4]
                break
            response = client.recv(5000).decode(FORMAT)
            data += response

    text_file = open(csv, "w")
    a = text_file.write(data)
    text_file.close()
    """
    data = pd.read_csv('test.csv', index_col=0)
    print("Grab name from Dataframe:\n" + data.iloc[0]["name"])
    """


message = send("get_video_database()")
if message[:4] == "<!d>":
    data_response(message, "test.csv")


# input()
# send("get_rating(4)")
# input()
# send("get_url(2)")

# Doesn't work with this send function
# send(DISCONNECT_MESSAGE)

"""
import socket
  
# take the server name and port name
host = 'local host'
port = 5000
  
# create a socket at server side
# using TCP / IP protocol
s = socket.socket(socket.AF_INET,
                  socket.SOCK_STREAM)
  
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  
# bind the socket with server
# and port number
s.bind(('', port))
  
# allow maximum 1 connection to
# the socket
s.listen(1)
  
# wait till a client accept
# connection
c, addr = s.accept()
  
# display client address
print("CONNECTION FROM:", str(addr))
  
# send message to the client after
# encoding into binary string
c.send(b"HELLO, How are you ?")
 
msg = "Bye.............."
c.send(msg.encode())
  
# disconnect the server
c.close()
"""