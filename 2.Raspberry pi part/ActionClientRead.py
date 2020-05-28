import socket, time
def Tcp_connect( HostIp, Port ):
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HostIp, Port))
    return
def Tcp_Read():
    a = ''
    b = b''
    while a != b'\r':
        a = s.recv(1)
        b = b + a
    return b

def Tcp_Close():
   s.close()
   return 
Tcp_connect( '192.168.31.7', 17098) # Replace with Your Server IP,port=17098
