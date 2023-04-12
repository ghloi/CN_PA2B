import socket
from packet import *
from udt import *
class GbN():
    def __init__(self):
        self.packetSize=1000
    def receive_packets(self,socket, address):
        expected_seq_num = 0
        received_packets = []
        recieved_sequence=[]
        
        print(f'Starting protocol')
        while True: #Start receiving packets. 
            try:
                print(f'Waiting for packet')
                packet, sender_address = recv(socket) #Extract packet sequence number and data
                seq_num, data=extract(packet)
                try:
                    eof=data.decode('utf-8')
                    if(eof=='EOF'): #If packet is EOF then we can stop. 
                        break
                except:
                    pass
                if seq_num == expected_seq_num: #If sequence number is expected, then save packet. 
                    print(f'Received packet {seq_num}')
                    packet=make(seq_num, make_empty())
                    send(packet, socket, sender_address) #Send ack. 
                    print(f'Appending packet #{seq_num}')
                    received_packets.append(data)
                    expected_seq_num +=1 #Increase expected seq num to wait for next packet. 
                    recieved_sequence.append(seq_num)
                else:
                    print(f'Received out-of-order packet {seq_num}. Expecting {expected_seq_num}')
                    try:
                        previous_seq=recieved_sequence[-1]
                    except:
                        previous_seq=-1
                    print(f'Sending back {previous_seq}')
                    packet=make(previous_seq, make_empty()) #If received unexpected packet then send previous ack. 
                    send(packet, socket, sender_address)
            except socket.timeout:
                print('Timeout waiting for packet')
                break
        return received_packets
    def begin(self, ip, portNumber):
    # Create a UDP socket and connect it to the server address
        print(f'Connecting to {ip} on port {portNumber}')
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = (ip, portNumber)
        client_socket.bind(('localhost',3560))
        print(f'Socket has been binded')
        # Receive packets
        received_packets = self.receive_packets(client_socket, server_address)
        
        # Close the socket once transmission is done
        client_socket.close()
        return received_packets