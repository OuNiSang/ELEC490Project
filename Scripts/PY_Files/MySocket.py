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
        totalsent = 0
        while totalsent < MSGLEN:
            sent = self.s.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

    def myreceive(self):
        chunks = []
        bytes_recd = 0
        while bytes_recd < MSGLEN:
            chunk = self.s.recv(min(MSGLEN - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return b''.join(chunks)
    
