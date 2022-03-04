import socket
MSGLEN = 40

class MySocket:

    def __init__(self, skt=None):
        
        if skt == None:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        else:
            self.s = skt;
    
    def bind(self, client, port):
        print("TBinding{0}{1}".format(client,port))
        self.s.bind((client, int(port)))
        self.s.listen(5)
    
    def connect(self, host, port): #For client 
        self.s.connect((host, int(port)))

    def mysend(self, msg):
        sent = self.s.send(msg.encode())
        if sent == 0:
            raise RuntimeError("socket connection broken")

