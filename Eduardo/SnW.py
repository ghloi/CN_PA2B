import socket
from packet import *
from udt import *
class Snw():
    def __init__(self):
        self.packetSize=1000
    def receive_packets(self,socket, address):
        expected_seq_num = 0
        received_packets = []
        ackDic={0:1,1:0}
        print(f'Starting protocol')
        while True: #Start receiving
            try:
                print(f'Waiting for packet')
                packet, sender_address = recv(socket)
                seq_num, data=extract(packet) #Receive packet and extract contents
                try:
                    eof=data.decode('utf-8')
                    if(eof=='EOF'): #If EOF has been received, we can stop receiving packets and save file. 
                        break
                except:
                    pass
                if seq_num == expected_seq_num: #If received expected packet, then save packet. 
                    print(f'Received packet {seq_num}') 
                    packet=make(seq_num, make_empty())
                    send(packet, socket, sender_address) #Send ack
                    received_packets.append(data)
                    expected_seq_num = ackDic[expected_seq_num]

                else:
                    print(f'Received out-of-order packet {seq_num}') #If received unexpected packet
                    packet=make(ackDic[expected_seq_num], make_empty()) #Then send previous ack. 
                    send(packet, socket, sender_address)
            except socket.timeout:
                print('Timeout waiting for packet')
                break
            
        return received_packets
    def begin(self, ip, portNumber): #Create socket. 
    # Create a UDP socket and connect it to the server address
        print(f'Connecting to {ip} on port {portNumber}')
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = (ip, portNumber)
        client_socket.bind(('localhost', 3560))
        print(f'Socket has been binded.')
        # Receive packets
        received_packets = self.receive_packets(client_socket, server_address)
        
        # Close the socket once transmission is done
        client_socket.close()
        return received_packets