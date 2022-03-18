#from wakeonlan import send_magic_packet
#send_magic_packet('D0-50-99-A7-88-AE')
#send_magic_packet('4C.CC.6A.2E.3C.94')
#send_magic_packet('9C.B6.D0.09.A8.EB')
#send_magic_packet('9E.B6.D0.09.A8.EB')
#send_magic_packet('AE.B6.D0.09.A8.EB')
#send_magic_packet('9C.B6.D0.09.A8.EC')

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
c.send(b"HELLO, How are you ? \
       Welcome to Akash hacking World")
 
msg = "Bye.............."
c.send(msg.encode())
  
# disconnect the server
c.close()
