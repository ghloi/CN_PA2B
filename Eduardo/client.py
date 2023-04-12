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
    def recieve(self): #Will start receiving packets depending on protocol selected
        if(self.protocol=='SnW'):
            print(f'Receiving using {self.protocol}')
            self.recieve_snw()
        else:
            self.recieve_goBackN()
        self.save_file()
    def recieve_snw(self):
        self.recievedPackets=self.SnWReceiver.begin(self.serverIp, self.serverPort) #SnW protocol
    def recieve_goBackN(self):
        self.recievedPackets=self.GbNReceiver.begin(self.serverIp, self.serverPort) #GnB protocol
        
    def save_file(self): #Method will take packets and save file. 
        print(f'Recieved {len(self.recievedPackets)} packets')
        with open(self.fileName, "wb") as f:
            print('Writing file')
            i=0
            for packet in self.recievedPackets:
                print(f'Writing packet {i}')
                i+=1
                f.write(packet)