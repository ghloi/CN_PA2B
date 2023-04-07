from SnW import *
class Client():
    def __init__(self, serverIp, serverPort, protocol, fileName):
        self.serverIp=serverIp
        self.serverPort=serverPort
        self.protocol=protocol
        self.fileName=fileName
        self.SnWReceiver=Snw()
        self.recievedPackets=[]
    def recieve(self):
        if(self.protocol=='SnW'):
            self.recieve_goBackn()
        else:
            self.recieve_goBackn()
    def recieve_goBackn(self):
        self.recievedPackets=self.SnWReceiver.begin(self.serverIp, self.serverPort)
        self.save_file()
        
    def save_file(self):
        with open(self.fileName, "w") as f:
            for packet in self.recievedPackets:
                f.write(packet.decode())