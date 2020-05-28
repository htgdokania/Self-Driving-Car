import socket
    
def Tcp_server_wait ( numofclientwait, port ):
    global s2
    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2.bind(('',port))
    s2.listen(numofclientwait)
    
def Tcp_server_next ( ):
    global s
    s = s2.accept()[0]
    
def Tcp_Write(D):
   s.send(D + b'\r')
   return 
   
def Tcp_Close( ):
   s.close()
   s2.close()
   return 

Tcp_server_wait ( 5, 17098 )
Tcp_server_next()