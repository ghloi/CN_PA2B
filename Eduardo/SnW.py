import socket
from packet import *
class Snw():
    def __init__(self):
        self.windowSize=4
        self.packetSize=1000
    def receive_packets(self,socket, address):
        expected_seq_num = 0
        received_packets = []
        ackDic={0:1,1:0}
        while True:
            try:
                packet, sender_address = socket.recvfrom(self.packetSize)
                seq_num, data=extract(packet)
                if seq_num == expected_seq_num:
                    print(f'Received packet {seq_num}')
                    packet=make(seq_num, make_empty())
                    socket.sendto(packet, address)
                    received_packets.append(data)
                    expected_seq_num = ackDic[expected_seq_num]
                else:
                    print(f'Received out-of-order packet {seq_num}')
            except socket.timeout:
                print('Timeout waiting for packet')
                break
            if len(received_packets) == self.windowSize:
                break
        return received_packets
    def begin(self, ip, portNumber):
    # create a UDP socket and connect it to the server address
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = (ip, portNumber)
        client_socket.connect(server_address)

        # receive packets
        received_packets = self.receive_packets(client_socket, server_address)
        
        # close the socket
        client_socket.close()
        return received_packets