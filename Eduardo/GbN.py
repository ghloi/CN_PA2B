import socket
from packet import *
class GbN():
    def __init__(self):
        self.packetSize=1000
    def receive_packets(self, socket, address):
        pass
    def receive_packets(self,socket, address):
        expected_seq_num = 0
        received_packets = []
        print(f'Starting protocol')
        while True:
            try:
                print(f'Waiting for packet')
                packet, sender_address = socket.recvfrom(self.packetSize)
                seq_num, data=extract(packet)
                try:
                    eof=data.decode()
                    if(eof=='EOF'):
                        break
                except:
                    pass
                if seq_num == expected_seq_num:
                    print(f'Received packet {seq_num}')
                    packet=make(seq_num, make_empty())
                    socket.sendto(packet, address)
                    received_packets.append(data)
                    expected_seq_num +=1
                else:
                    print(f'Received out-of-order packet {seq_num}')
            except socket.timeout:
                print('Timeout waiting for packet')
                break
            
        return received_packets
    def begin(self, ip, portNumber):
    # create a UDP socket and connect it to the server address
        print(f'Connecting to {ip} on port {portNumber}')
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = (ip, portNumber)
        client_socket.connect(server_address)
        print(f'Connection successful')
        # receive packets
        received_packets = self.receive_packets(client_socket, server_address)
        
        # close the socket
        client_socket.close()
        return received_packets