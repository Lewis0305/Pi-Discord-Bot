#from wakeonlan import send_magic_packet
#send_magic_packet('D0-50-99-A7-88-AE')
#send_magic_packet('4C.CC.6A.2E.3C.94')
#send_magic_packet('9C.B6.D0.09.A8.EB')
#send_magic_packet('9E.B6.D0.09.A8.EB')
#send_magic_packet('AE.B6.D0.09.A8.EB')
#send_magic_packet('9C.B6.D0.09.A8.EC')

import socket
import pandas as pd

HEADER = 64
PORT = 5070
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "169.254.27.180"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

print("Connected")
def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print("Sent")
    # TODO This can only send 5000 rows (Should only add new entries (requires change to the file write))
    response = client.recv(5000).decode(FORMAT)
    print(response)
    text_file = open("test.csv", "w")
    a = text_file.write(response)
    text_file.close()

    data = pd.read_csv('test.csv', index_col=0)
    print(data.iloc[0]["name"])


send("get_video_database()")
input()
send("get_rating(4)")
input()
send("get_url(2)")

send(DISCONNECT_MESSAGE)

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