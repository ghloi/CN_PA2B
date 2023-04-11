from SnW import *
from GbN import *
class Client():
    def __init__(self, serverIp, serverPort, protocol, fileName):
        self.serverIp=serverIp
        self.serverPort=serverPort
        self.protocol=protocol
        self.fileName=fileName
        self.SnWReceiver=Snw()
        self.GbNReceiver=GbN()
        self.recievedPackets=[]
    def recieve(self):
        if(self.protocol=='SnW'):
            print(f'Receiving using {self.protocol}')
            self.recieve_snw()
        else:
            self.recieve_goBackN()
        self.save_file()
    def recieve_snw(self):
        self.recievedPackets=self.SnWReceiver.begin(self.serverIp, self.serverPort)
    def recieve_goBackN(self):
        self.receievedPackets=self.GbNReceiver.begin(self.serverIp, self.serverPort)
        
    def save_file(self):
        with open(self.fileName, "wb") as f:
            i=0
            for packet in self.recievedPackets:
                print(f'Writing packet {i}')
                i+=1
                f.write(packet)